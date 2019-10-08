# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class NoPlasticDetectPlugin(octoprint.plugin.StartupPlugin):
        def on_after_startup(self):
                self._logger.info("Nørd'o'tekets filament_out detektor plugin")

__plugin_name__ = "NoPlasticDetect"                
__plugin_implementation__ = NoPlasticDetectPlugin()
                            
