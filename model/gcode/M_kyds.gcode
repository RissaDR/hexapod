;FLAVOR:RepRap
;TIME:0
;Generated with Cura_SteamEngine 2.3.1
M190 S60
M104 S200
M109 S200
G21 ;metric values
G90 ;absolute positioning
G92 E0 ;zero the extruded length
M107 ;start with the fan off
G1 X90 Y200 F6000 ;go to the middle of the front

G92 E0 ;zero the extruded length
G1 X150 E10 F300 ; make a thick line to prime extruder
G92 E0 ; reset extruder
;LAYER_COUNT:0
G1 F1500 E-6.5
M107
M104 S0 ;extruder heater off
M140 S0 ;heated bed heater off (if you have it)
M107 ;carriage fan off
G91 ;relative positioning
G1 Z10 ;Move up Z 10mm
G90 ;back to absolute mode
G1 E-1 F1200 ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G92 E0 ;zero the extruded length
G1 Y10 F5000 ;Move Y to front
M84 ;steppers off
M104 S0
;End of Gcode
;SETTING_3 {"global_quality": "[general]\\nversion = 2\\nname = empty\\ndefiniti
;SETTING_3 on = mendel90\\n\\n[metadata]\\ntype = quality_changes\\nquality_type
;SETTING_3  = normal\\n\\n[values]\\nmaterial_bed_temperature = 60\\nbrim_width 
;SETTING_3 = 5\\nraft_surface_layers = 1\\nadhesion_type = skirt\\nlayer_height 
;SETTING_3 = 0.2\\nraft_airgap = 0.2\\nsupport_enable = True\\n\\n"}
