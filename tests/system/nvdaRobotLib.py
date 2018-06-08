from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.Process import Process
import sendKey

builtIn = BuiltIn()
os = OperatingSystem()
process = Process()

class nvdaRobotLib(object):

	def __init__(self):
		self.nvdaSpy = None
		self.nvdaHandle = None


	def copy_in_system_test_spy(self):
		"""Equiv robot text:
		Copy File  tests/system/systemTestSpy.py  source/globalPlugins/
		"""
		os.copy_file("tests/system/systemTestSpy.py", "source/globalPlugins/")


	def _startNVDAProcess(self):
		"""Equiv robot text:
		Start Process  pythonw nvda.pyw --debug-logging  cwd=source  shell=true  alias=nvdaAlias
		"""
		self.nvdaHandle = handle = process.start_process(
			"pythonw nvda.pyw --debug-logging",
			cwd='source',
			shell=True,
			alias='nvdaAlias'
		)
		return handle


	def _connectToRemoteServer(self):
		"""Equiv robot text:
		Import Library  Remote         WITH NAME    nvdaSpy
		"""
		builtIn.import_library(
				"Remote",
				'http://127.0.0.1:8270',
				"WITH NAME",
				"nvdaSpy"
			)
		self.nvdaSpy = builtIn.get_library_instance("nvdaSpy")


	def start_NVDA(self):
		print "*WARN* copy plugin"
		self.copy_in_system_test_spy()
		print "*WARN* start NVDA process"
		nvdaProcessHandle = self._startNVDAProcess()
		print "*WARN* check if running"
		process.process_should_be_running(nvdaProcessHandle)
		print "*WARN* connect to remote server"
		self._connectToRemoteServer()
		print "*WARN* wait for NVDA start-up to complete"
		self.wait_for_NVDA_startup_to_complete()
		print "*WARN* done"
		return nvdaProcessHandle


	def wait_for_NVDA_startup_to_complete(self):
		while not self.nvdaSpy.run_keyword("is_NVDA_startup_complete", [], {}):
			builtIn.sleep(0.1)

	def quit_NVDA(self):
		"""send quit NVDA keys
			sleep  1
			send enter key
			nvdaSpy.Stop Remote Server
			Wait For Process  nvdaAlias
		"""
		print "*WARN* send quit NVDA keys"
		sendKey.send_quit_NVDA_keys()
		print "*WARN* sleep"
		builtIn.sleep(1.0)
		print "*WARN* send enter key"
		sendKey.send_enter_key()
		print "*WARN* stop remote server"
		self.nvdaSpy.run_keyword("stop_remote_server", [], {})
		print "*WARN* wait for NVDA process"
		return process.wait_for_process(self.nvdaHandle)
