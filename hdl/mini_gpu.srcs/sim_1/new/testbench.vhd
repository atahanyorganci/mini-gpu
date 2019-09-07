----------------------------------------------------------------------------------
-- Engineer: Atahan Yorganci
-- Create Date: 29.08.2019
-- Module Name: Testbench - Behavioral
-- Project Name: Mini GPU
-- Target Devices: BASYS 3
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity testbench is
end testbench;

architecture Behavioral of testbench is

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

	-- Constants
	type DataArray is array (0 to 11) of std_logic_vector(9 downto 0);
	constant c_CLOCK_FREQ : integer   := 100_000_000;
	constant c_BAUDRATE   : integer   := 9600;
	constant c_TICK_COUNT : integer   := c_CLOCK_FREQ / c_BAUDRATE;
	constant c_DATA       : DataArray := (
		"1000000010",
		-- RGB
		"1000011110",
		"1000000110",
		"1000000010",
		-- HCorner
		"1111100000",
		"1000000000",
		-- VCorner
		"1000011110",
		"1000000010",
		-- Width
		"1000000100",
		"1000000010",
		-- Height
		"1000000010",
		"1000000010"
	);
	constant c_DATA_COUNT : integer   := 12;

	-- Control
	signal s_Clock     : std_logic;
	signal s_Reset     : std_logic;
	signal s_TickCount : integer;
	signal s_Index     : integer;
	signal s_DataCount : integer;

	-- UART RX
	signal s_Rx      : std_logic;
	signal s_RxRead  : std_logic := '0';
	signal s_RxData  : std_logic_vector(7 downto 0);
	signal s_RxReady : std_logic;

	-- Bank
	signal s_HPos  : integer;
	signal s_VPos  : integer;
	signal s_Color : std_logic_vector(11 downto 0);

	-- Parser
	signal s_ConfigSelect : std_logic_vector(1 downto 0);
	signal s_ConfigEn     : std_logic_vector(0 downto 0);
	signal s_ConfigAddr   : std_logic_vector(2 downto 0);
	signal s_ConfigData   : std_logic_vector(15 downto 0);
	signal s_ConfigDone   : std_logic;

begin
	my_bank : bank
		port map(
			p_Clock        => s_Clock,
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
			p_Clock        => s_Clock,
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
			g_BAUDRATE   => 9600,
			g_CLOCK_FREQ => 100000000
		)
		port map(
			p_ReadClock => s_Clock,
			p_Clock     => s_Clock,
			p_Reset     => s_Reset,
			p_Rx        => s_Rx,
			p_RxRead    => s_RxRead,
			o_RxData    => s_RxData,
			o_RxReady   => s_RxReady
		);

	position : process(s_Clock, s_Reset) is
	begin
		if s_Reset = '1' then
			s_HPos <= 0;
			s_VPos <= 0;
		elsif rising_edge(s_Clock) then
			if s_HPos = 800 then
				s_HPos <= 0;
				if s_VPos = 600 then
					s_VPos <= 0;
				else
					s_VPos <= s_VPos + 1;
				end if;
			else
				s_HPos <= s_HPos + 1;
			end if;

		end if;
	end process position;

	rx : process(s_Clock, s_Reset) is
	begin
		if s_Reset = '1' then
			s_TickCount <= 0;
			s_DataCount <= 0;
			s_Index     <= 0;
			s_Rx        <= '1';
		elsif rising_edge(s_Clock) then
			if s_DataCount = c_DATA_COUNT then
				s_Rx <= '1';
			elsif s_TickCount < c_TICK_COUNT then
				s_TickCount <= s_TickCount + 1;
			else
				if s_Index < 9 then
					s_Index <= s_Index + 1;
				else
					s_DataCount <= s_DataCount + 1;
					s_Index <= 0;
				end if;
				s_Rx <= c_DATA(s_DataCount)(s_Index);
				s_TickCount <= 0;
			end if;
		end if;
	end process rx;

	control : process
	begin
		s_Reset <= '1';
		wait for 100 ns;
		s_Reset <= '0';
		wait;
	end process;

	clock : process
	begin
		s_Clock <= '1';
		wait for 5 ns;
		s_Clock <= '0';
		wait for 5 ns;
	end process;

end Behavioral;
