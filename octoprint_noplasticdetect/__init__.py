# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events
import RPi.GPIO as GPIO
from time import sleep
from flask import jsonify

class NoPlasticDetectPlugin(octoprint.plugin.StartupPlugin,
                            octoprint.plugin.EventHandlerPlugin,
                            octoprint.plugin.TemplatePlugin,
                            octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.BlueprintPlugin):

        def initialize(self):
                self._logger.info("Running RPi.GPIO version '{0}'".format(GPIO.VERSION))
                if GPIO.VERSION < "0.6":       # Need at least 0.6 for edge detection
                        raise Exception("RPi.GPIO must be greater than 0.6")
                else:
                        self._logger.info("GPIO version OK")
                GPIO.setwarnings(False)        # Disable GPIO warnings
                                                
        def on_after_startup(self):
                self._logger.info("Nørd'o'tekets filament_out detektor plugin")
                self._setup_filament_sensor()

        @octoprint.plugin.BlueprintPlugin.route("/status", methods=["GET"])
        def check_status(self):
                status="-1"
                if self.sensor_enabled():
                        status = "0" if self.no_filament() else "1"
                return jsonify(status=status)
        

        @property
        def pin(self):
                return int(self._settings.get(["pin"]))

        @property
        def NormallyOpen(self):
                return int(self._settings.get(["NormallyOpen"]))


        def _setup_filament_sensor(self):
                if self.sensor_enabled():
                        self._logger.info("Configuring the RPi GPIO")
                        GPIO.setmode(BCM)
                        self._logger.info("GPIO%s is configured as input with internal pull-up enabled"%self.pin)
                        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                else:
                        self-logger("Plugin not enabled.")

        def get_settings_defaults(self):
                return dict(
                        pin = -1, #GPIO pin, -1 = plugin is disabled
                        NormallyOpen = 1 # is the switch open or closen when no filament (default=closed)
                )

        def on_settings_save(self, data):
                octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
                self._setup_filament_sensor()


        def no_filament(self):
                return GPIO.input(self.pin) != self.NormallyOpen

        def sensor_enabled(self):
                return self.pin != -1

        def get_template_configs(self):
            return [dict(type="settings", custom_bindings=False)]



        def on_event(self, event, payload):
                if event is Events.PRINT_STARTED and self.no_filament():
                        self._logger.info("Printing aborted: no filament detected!")
                        self._printer.cancel_print()
                # Enable sensor
                if event in (
                                Events.PRINT_STARTED,
                                Events.PRINT_RESUMED
                ):
                        self._logger.info("%s: Enabling filament sensor." % (event))
                        if self.sensor_enabled():
                        #        self.triggered = 0 # reset triggered state
                                GPIO.remove_event_detect(self.pin)
                                GPIO.add_event_detect(
                                        self.pin, GPIO.BOTH,
                                        callback=self.sensor_callback,
                         #               bouncetime=self.bounce
                                )
                # Disable sensor
                elif event in (
                                Events.PRINT_DONE,
                                Events.PRINT_FAILED,
                                Events.PRINT_CANCELLED,
                                Events.ERROR
                ):
                        self._logger.info("%s: Disabling filament sensor." % (event))
                        GPIO.remove_event_detect(self.pin)
                                                                                                                                        

        def sensor_callback(self, _):

                if self.no_filament:
                        self._logger.info("Out of filament detected!!!")
                        ## SEND PAUSE HER
                else:
                        self._logger.info("Filament detected.")

__plugin_name__ = "No Plastic Detect"
__plugin_version__ = "0.9.0"
                        
def __plugin_load():
        global __plugin_implementation__
        __plugin_implementation__ = NoPlasticDetectPlugin()
                            
