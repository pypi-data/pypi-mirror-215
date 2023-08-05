from __future__ import annotations
from collections.abc import Callable

from .request import Request, RequestActions
from .message import EventMessage, Message, MessageModule, MessageType, CommandMessage
from .enums import EventOperationID, AgentAIMode, AgentTriggerType, CommandOperationID, \
                LogCommand, DBMCommandParameter, DBMTable, DBMCommand
from .utils import unpack_buffer_to_list, b642b
from .timer import Timer


class Agent():
    def __init__(self, gateway: "Gateway", device_name: str) -> None:
        self.device_name = device_name
        self.gateway = gateway

        self._active_label = None

        self._wait_response = {}

        self._on_log_handlers: dict[str, Callable[[Agent, str], None]] = {}
        self._on_event_handlers: dict[str, Callable[[Agent, EventOperationID, dict], None]] = {}

        self._on_train_done_handlers: dict[str, Callable[[Agent, dict], None]] = {}
        self._on_final_process_done: dict[str, Callable[[Agent, dict], None]] = {}
        self._on_infer_done_handlers: dict[str, Callable[[Agent, dict], None]] = {}

    def handle_message(self, msg: dict) -> None:
        if "header" in msg:
            mod = MessageModule(msg['header']['mod'])
            typ = MessageType(msg['header']['typ'])
            msg_id = msg["header"]["id"]

            data: dict = None
            if "payloads" in msg and len(msg["payloads"]):
                data = msg["payloads"][0]['data']

            if msg_id in self._wait_response:
                self._wait_response[msg_id] = data

            if typ == MessageType.EVENT:
                operation = EventOperationID(msg['header']['op'])
                if mod == MessageModule.LOG:
                    if operation == EventOperationID.EVT_EXT_LOG:
                        content = data.get("msg", "")
                        if content == "EVT_INT_TRAIN_DONE":
                            for callback in self._on_train_done_handlers.values():
                                callback(self, data)
                        else:
                            for callback in self._on_log_handlers.values():
                                callback(self, content)
                else:
                    if operation == EventOperationID.EVT_INT_INFER_DONE:
                        for callback in self._on_infer_done_handlers.values():
                            callback(self, data)
                    elif operation == EventOperationID.EVT_INT_FINAL:
                        for callback in self._on_final_process_done.values():
                            callback(self, data)
                    for callback in self._on_event_handlers.values():
                        callback(self, operation, data)

    def remove_observer(self, dict_obj_name, idx):
        if not hasattr(self, dict_obj_name):
            return 
        dict_obj = getattr(self, dict_obj_name)
        if hasattr(dict_obj, idx):
            delattr(getattr(self, dict_obj_name), idx)

    def set_active_label(self, label_id: int) -> None:
        self._active_label = label_id

    def on_log(self, callback: Callable[["Agent", str], None]) -> None:
        cb_id = f"onlog-{len(self._on_log_handlers.keys())}"
        self._on_log_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_log_handlers", cb_id)

    def on_event(self, callback: Callable[["Agent", EventOperationID, dict], None]) -> None:
        cb_id = f"onevent-{len(self._on_log_handlers.keys())}"
        self._on_event_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_event_handlers", cb_id)

    def on_training_done(self, callback: Callable[["Agent", dict], None]) -> None:
        cb_id = f"ontraindone-{len(self._on_log_handlers.keys())}"
        self._on_train_done_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_train_handlers", cb_id)

    def on_inference_done(self, callback: Callable[["Agent", dict], None]) -> None:
        cb_id = f"oninferdone-{len(self._on_log_handlers.keys())}"
        self._on_infer_done_handlers[cb_id] = callback
        return lambda: self.remove_observer("_on_infer_done_handlers", cb_id)

    def on_final_process_done(self, callback: Callable[["Agent", dict], None]) -> None:
        cb_id = f"onfinaldone-{len(self._on_log_handlers.keys())}"
        self._on_final_process_done[cb_id] = callback
        return lambda: self.remove_observer("_on_final_process_done", cb_id)

    def send_message(self, message: Message, sync: bool = False):
        self.gateway.Send(Request(
            RequestActions.ACT_SEND_TO_DEVICE, 
            self.device_name, 
            message.to_dict()
        ))

        if sync:
            return self.wait_command_response(message)
        
        return None

    def subscribe(self):
        self.gateway.Send(Request(
            RequestActions.ACT_SUB_TO_DEVICE, 
            self.device_name
        ))        

    def send_chunk(self, source_id: int, chunk: list[float]) -> None:
        msg = EventMessage(EventOperationID.EVT_EXT_DATA_IN)\
            .add_payload(source_id, "<f", chunk)
        self.send_message(msg)

    def send_data(self, source_id: int, data: list[float], chunk_size: int, chunk_rate: int) -> None:
        sent_data = 0
        start_idx = 0
        end_idx = chunk_size
        chunk_period = 1 / chunk_rate
        data_len = len(data)
        while sent_data < len(data):
            time_1 = Timer.get_elapsed_time()
            self.send_chunk(source_id, data[start_idx:end_idx])
            sent_data += chunk_size
            send_time = Timer.get_elapsed_time() - time_1
            start_idx += chunk_size
            end_idx += chunk_size
            if end_idx > data_len:
                end_idx = data_len - 1
            Timer.wait(chunk_period - send_time)

    def set_ai_mode(self, mode: AgentAIMode, active_label: int = None) -> None:
        data = [mode.value]
        if mode == AgentAIMode.APP_AI_MODE_ENROLLEMENT:
            data += [1, active_label]
        msg = EventMessage(EventOperationID.EVT_EXT_CUSTOM_2)\
            .add_payload(data)
        self.send_message(msg)

    def trigger(self, trigger_type: AgentTriggerType) -> None:
        msg = EventMessage(EventOperationID.EVT_EXT_CUSTOM_1)\
            .add_payload([trigger_type.value])
        self.send_message(msg)

    def kill(self) -> None:
        self.trigger(AgentTriggerType.TRIGGER_KILL)

    def correct(self, ground_truth: float | int, position: int = 0, remove: bool = False):
        msg = EventMessage(EventOperationID.EVT_EXT_CUSTOM_2)\
            .add_payload([3, remove, position, ground_truth])
        self.send_message(msg)

    def wait_command_response(self, msg: Message, timeout: int = 10000):
        msg_id = msg.header.id
        self._wait_response[msg_id] = None

        sleeptime = 0.001
        start_time = Timer.get_elapsed_time()
        while msg_id in self._wait_response and self._wait_response[msg_id] is None:
            elapsed_time = Timer.get_elapsed_time() - start_time
            if elapsed_time > timeout:
                raise Exception("Command message Timeout")
            Timer.wait(sleeptime)

        return_value = self._wait_response[msg_id]
        del self._wait_response[msg_id]
        return return_value

    # OTA 
    def get_kpi(self):
        msg = CommandMessage(CommandOperationID.CMD_GET, MessageModule.LOG)
        msg.add_payload(LogCommand.LOG_GET_KPI.value)
        data: dict = self.send_message(msg, sync=True)

        if "number" not in data:
            raise Exception("Missing number in data")
        
        nbkpis = data.get("number")
        kpi_list = []
        for i in range(nbkpis):
            msg = CommandMessage(CommandOperationID.CMD_START, MessageModule.LOG)
            msg.add_payload(LogCommand.LOG_GET_KPI.value, i)
            kpi = self.send_message(msg, sync=True)
            kpi_list.append({
                "id": kpi.get("id", 0),
                "description": kpi["description"],
                "value": kpi["value"],
                "type": kpi["typ"]
            })

        return kpi_list
    
    def export_dataset(self) -> list:
        datasets = []
        for data in self.export_table_data(DBMTable.DBM_DAT): 
            val = data.get("record")
            if val is not None:
                data["record"] = unpack_buffer_to_list(
                    b642b(val),

                )
            datasets.append(data)
        return datasets

    def export_vm_list(self) -> list:
        return self.export_table_data(DBMTable.DBM_VM)
    
    def export_tables(self) -> list:
        msg = CommandMessage(CommandOperationID.CMD_GET, MessageModule.DBM)
        msg.add_payload(DBMCommandParameter.DBM_PARAM_INFO.value)
        data = self.send_message(msg, sync=True)

        return data.get("tables", [])
    
    def export_table_data(self, data_type: DBMTable) -> list:
        tables = self.export_tables()
        results = []

        for table in tables:
            if table.get("typ") != data_type.value:
                continue

            for i in range(table.get("count", 0)):
                msg = CommandMessage(CommandOperationID.CMD_START, MessageModule.DBM)
                msg.add_payload(DBMCommand.DBM_EXPORT_ROW.value, table.get("handle"), "", i)
                data = self.send_message(msg, sync=True)
                attr = data.get("attributes")
                if attr is not None:
                    results.append(attr)

        return results
