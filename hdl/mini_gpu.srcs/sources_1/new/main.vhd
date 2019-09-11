----------------------------------------------------------------------------------
-- Engineer: Atahan Yorganci
-- Create Date: 29.08.2019
-- Module Name: Main - Behavioral
-- Project Name: Mini GPU
-- Target Devices: BASYS 3
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity main is
	Port(
		CLOCK     : in  std_logic;
		RESET     : in  std_logic;
		RX        : in  std_logic;
		--		TX        : out std_logic;
		VGA_VS    : out std_logic;
		VGA_HS    : out std_logic;
		VGA_RED   : out std_logic_vector(3 downto 0);
		VGA_BLUE  : out std_logic_vector(3 downto 0);
		VGA_GREEN : out std_logic_vector(3 downto 0)
	);
end main;

architecture Behavioural of main is

	component vga_driver
		port(
			p_Clock    : in  std_logic;
			p_Reset    : in  std_logic;
			p_Color    : in  std_logic_vector(11 downto 0);
			o_HPos     : out integer;
			o_VPos     : out integer;
			o_VGAHS    : out std_logic;
			o_VGAVS    : out std_logic;
			o_VGARed   : out std_logic_vector(3 downto 0);
			o_VGAGreen : out std_logic_vector(3 downto 0);
			o_VGABlue  : out std_logic_vector(3 downto 0)
		);
	end component vga_driver;

	component clock_wizard
port
 (
  vga_clock          : out    std_logic;
  uart_clock          : out    std_logic;
  reset             : in     std_logic;
  locked            : out    std_logic;
  clock_in           : in     std_logic
 );
end component;

	component parser
		port(
			p_Clock        : in  std_logic;
			p_Reset        : in  std_logic;
			p_RxData       : in  std_logic_vector(7 downto 0);
			p_RxReady      : in  std_logic;
			o_RxRead       : out std_logic;
			o_ConfigSelect : out std_logic_vector(1 downto 0);
			o_ConfigEn     : out std_logic_vector(0 downto 0);
			o_ConfigAddr   : out std_logic_vector(2 downto 0);
			o_ConfigData   : out std_logic_vector(15 downto 0);
			o_ConfigDone   : out std_logic
		);
	end component parser;

	component uart_rx
		generic(
			g_BAUDRATE   : integer;
			g_CLOCK_FREQ : integer
		);
		port(
			p_Clock     : in  std_logic;
			p_ReadClock : in  std_logic;
			p_Reset     : in  std_logic;
			p_Rx        : in  std_logic;
			p_RxRead    : in  std_logic;
			o_RxData    : out std_logic_vector(7 downto 0);
			o_RxReady   : out std_logic
		);
	end component uart_rx;

	component bank
		port(
			p_Clock        : in  std_logic;
			p_Reset        : in  std_logic;
			p_HPos         : in  integer range 0 to 65535;
			p_VPos         : in  integer range 0 to 65535;
			p_ConfigEn     : in  std_logic_vector(0 downto 0);
			p_ConfigAddr   : in  std_logic_vector(2 downto 0);
			p_ConfigData   : in  std_logic_vector(15 downto 0);
			p_ConfigDone   : in  std_logic;
			p_ConfigSelect : in  std_logic_vector(1 downto 0);
			o_Color        : out std_logic_vector(11 downto 0)
		);
	end component bank;

	constant c_BAUDRATE   : integer := 115200;
	constant c_CLOCK_FREQ : integer := 200000000;

	-- Clock Wizard
	signal s_VGAClock  : std_logic;
	signal s_UARTClock : std_logic;
	signal s_Reset     : std_logic;
	signal s_Locked    : std_logic;

	-- VGA
	signal s_HPos  : integer;
	signal s_VPos  : integer;
	signal s_Color : std_logic_vector(11 downto 0);

	-- UART TX
	--	signal s_TxData  : std_logic_vector(7 downto 0);
	--	signal s_TxWrite : std_logic;
	--	signal s_TxReady : std_logic;

	-- UART RX
	signal s_RxData  : std_logic_vector(7 downto 0);
	signal s_RxRead  : std_logic;
	signal s_RxReady : std_logic;

	-- Parser
	signal s_ConfigSelect : std_logic_vector(1 downto 0);
	signal s_ConfigEn     : std_logic_vector(0 downto 0);
	signal s_ConfigAddr   : std_logic_vector(2 downto 0);
	signal s_ConfigData   : std_logic_vector(15 downto 0);
	signal s_ConfigDone   : std_logic;

begin
	s_Reset <= not s_Locked;

	my_vga : vga_driver
		port map(
			p_Clock    => s_VGAClock,
			p_Reset    => s_Reset,
			p_Color    => s_Color,
			o_HPos     => s_HPos,
			o_VPos     => s_VPos,
			o_VGAHS    => VGA_HS,
			o_VGAVS    => VGA_VS,
			o_VGARed   => VGA_RED,
			o_VGAGreen => VGA_GREEN,
			o_VGABlue  => VGA_BLUE
		);

	my_bank : bank
		port map(
			p_Clock        => s_VGAClock,
			p_Reset        => s_Reset,
			p_HPos         => s_HPos,
			p_VPos         => s_VPos,
			p_ConfigEn     => s_ConfigEn,
			p_ConfigAddr   => s_ConfigAddr,
			p_ConfigData   => s_ConfigData,
			p_ConfigDone   => s_ConfigDone,
			p_ConfigSelect => s_ConfigSelect,
			o_Color        => s_Color
		);

	my_parser : parser
		port map(
			p_Clock        => s_VGAClock,
			p_Reset        => s_Reset,
			p_RxData       => s_RxData,
			p_RxReady      => s_RxReady,
			o_RxRead       => s_RxRead,
			o_ConfigSelect => s_ConfigSelect,
			o_ConfigEn     => s_ConfigEn,
			o_ConfigAddr   => s_ConfigAddr,
			o_ConfigData   => s_ConfigData,
			o_ConfigDone   => s_ConfigDone
		);

	my_rx : uart_rx
		generic map(
			g_BAUDRATE   => c_BAUDRATE,
			g_CLOCK_FREQ => c_CLOCK_FREQ
		)
		port map(
			p_ReadClock => s_VGAClock,
			p_Clock     => s_UARTClock,
			p_Reset     => s_Reset,
			p_Rx        => RX,
			p_RxRead    => s_RxRead,
			o_RxData    => s_RxData,
			o_RxReady   => s_RxReady
		);

	my_clock_wizard : clock_wizard
   port map ( 
   vga_clock => s_VGAClock,
   uart_clock => s_UARTClock,            
   reset => RESET,
   locked => s_Locked,
   clock_in => CLOCK
 );

end architecture Behavioural;
