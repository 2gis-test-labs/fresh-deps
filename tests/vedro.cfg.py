import vedro
import vedro_jj
import vedro_valera_validator as valera_validator


class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class RichReporter(vedro.Config.Plugins.RichReporter):
            enabled = True
            show_timings = True
            show_scenario_spinner = False

        class ValeraValidator(valera_validator.ValeraValidator):
            enabled = True

        class RemoteMock(vedro_jj.RemoteMock):
            enabled = True
            threaded = False
            host = "localhost"
            port = 8080
