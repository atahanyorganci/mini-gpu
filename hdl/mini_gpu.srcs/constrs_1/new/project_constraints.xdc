# Clock
set_property PACKAGE_PIN W5 [get_ports CLOCK]
set_property IOSTANDARD LVCMOS33 [get_ports CLOCK]
create_clock -period 10.000 -name sys_clk_pin -waveform {0.000 5.000} -add [get_ports CLOCK]

# Switches
set_property PACKAGE_PIN R2 [get_ports RESET]
set_property IOSTANDARD LVCMOS33 [get_ports RESET]

# VGA Connector
set_property PACKAGE_PIN G19 [get_ports {VGA_RED[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_RED[0]}]
set_property PACKAGE_PIN H19 [get_ports {VGA_RED[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_RED[1]}]
set_property PACKAGE_PIN J19 [get_ports {VGA_RED[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_RED[2]}]
set_property PACKAGE_PIN N19 [get_ports {VGA_RED[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_RED[3]}]
set_property PACKAGE_PIN N18 [get_ports {VGA_BLUE[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_BLUE[0]}]
set_property PACKAGE_PIN L18 [get_ports {VGA_BLUE[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_BLUE[1]}]
set_property PACKAGE_PIN K18 [get_ports {VGA_BLUE[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_BLUE[2]}]
set_property PACKAGE_PIN J18 [get_ports {VGA_BLUE[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_BLUE[3]}]
set_property PACKAGE_PIN J17 [get_ports {VGA_GREEN[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_GREEN[0]}]
set_property PACKAGE_PIN H17 [get_ports {VGA_GREEN[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_GREEN[1]}]
set_property PACKAGE_PIN G17 [get_ports {VGA_GREEN[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_GREEN[2]}]
set_property PACKAGE_PIN D17 [get_ports {VGA_GREEN[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {VGA_GREEN[3]}]
set_property PACKAGE_PIN P19 [get_ports VGA_HS]
set_property IOSTANDARD LVCMOS33 [get_ports VGA_HS]
set_property PACKAGE_PIN R19 [get_ports VGA_VS]
set_property IOSTANDARD LVCMOS33 [get_ports VGA_VS]


# USB-RS232 Interface
set_property PACKAGE_PIN B18 [get_ports RX]
set_property IOSTANDARD LVCMOS33 [get_ports RX]
#set_property PACKAGE_PIN A18 [get_ports TX]
#set_property IOSTANDARD LVCMOS33 [get_ports TX]