# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events
import RPi.GPIO as GPIO
from time import sleep


class NoPlasticDetectPlugin(octoprint.plugin.StartupPlugin,
                            octoprint.plugin.TemplatePlugin,
                            octoprint.plugin.SettingsPlugin):

        def initialize(self):
                self._logger.info("Running RPi.GPIO version '{0}'".format(GPIO.VERSION))
                if GPIO.VERSION < "0.6":       # Need at least 0.6 for edge detection
                        raise Exception("RPi.GPIO must be greater than 0.6")
                GPIO.setwarnings(False)        # Disable GPIO warnings
                                                
        def on_after_startup(self):
                self._logger.info("Nørd'o'tekets filament_out detektor plugin")


        @property
        def pin(self):
                return int(self._settings.get(["pin"]))
                

        def _setup_filament_sensor(self):
                if self.sensor_enabled():
                        self._logger.info("Configuring the RPi GPIO")
                        GPIO.setmode(BCM)
                        self._logger.info("GPIO%s is configured as input with internal pull-up enabled"%self.pin)
                        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                else:
                        self-logger("Plugin not enabled.")

        def get_settings_default(self):
                return dict(
                        pin = -1, #GPIO pin, -1 = plugin is disabled
                        NormallyOpen = 1 # is the switch open or closen when no filament (default=closed)
                )

        def on_settings_save(self, data):
                octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
                self._setup_filament_sensor()


        def no_filament(self):
                return GPIO.input(self.pin) != self.NormallyOpen

        

        def get_template_configs(self):
            return [
            #        dict(type="navbar", custom_bindings=False),
                    dict(type="settings", custom_bindings=False)
            ]

                
                                    
__plugin_name__ = "NoPlasticDetect"                
__plugin_implementation__ = NoPlasticDetectPlugin()
                            
