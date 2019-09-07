-- Engineer: Atahan Yorganci
-- Create Date: 29.08.2019
-- Module Name: UART RX - Behavioral
-- Project Name: Mini GPU
-- Target Devices: BASYS 3
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity uart_rx is
	Generic(
		g_BAUDRATE   : integer := 9600;
		g_CLOCK_FREQ : integer := 100000000
	);
	Port(
		p_Clock     : in  std_logic;
		p_ReadClock : in  std_logic;
		p_Reset     : in  std_logic;
		p_Rx        : in  std_logic;
		p_RxRead    : in  std_logic;
		o_RxData    : out std_logic_vector(7 downto 0);
		o_RxReady   : out std_logic
	);
end uart_rx;

architecture Behavioral of uart_rx is

	COMPONENT fifo
		PORT(
			rst        : IN  STD_LOGIC;
			wr_clk     : IN  STD_LOGIC;
			rd_clk     : IN  STD_LOGIC;
			din        : IN  STD_LOGIC_VECTOR(7 DOWNTO 0);
			wr_en      : IN  STD_LOGIC;
			rd_en      : IN  STD_LOGIC;
			dout       : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
			full       : OUT STD_LOGIC;
			wr_ack     : OUT STD_LOGIC;
			empty      : OUT STD_LOGIC;
			prog_empty : OUT STD_LOGIC
		);
	END COMPONENT;

	type State is (Idle, Start, Data, Stop);

	constant c_TICK_COUNT     : integer := g_CLOCK_FREQ / g_BAUDRATE;
	constant c_SAMPLE_POINT01 : integer := c_TICK_COUNT / 6;
	constant c_SAMPLE_POINT02 : integer := c_TICK_COUNT / 2;
	constant c_SAMPLE_POINT03 : integer := 5 * c_TICK_COUNT / 6;

	-- FIFO
	signal s_RxFull : std_logic;

	-- FSM
	signal s_State : State;

	-- RX
	signal s_Rx          : std_logic;
	signal s_RxCount     : integer;
	signal s_RxData      : std_logic_vector(7 downto 0);
	signal s_RxEmpty     : std_logic;
	signal s_RxIndex     : integer range 0 to 15;
	signal s_RxSample    : std_logic_vector(2 downto 0);
	signal s_RxProgEmpty : std_logic;
	signal s_RxWrite     : std_logic;

	signal s_RxWriteAck : STD_LOGIC;

begin

	o_RxReady <= not s_RxProgEmpty;

	rx_fifo : fifo
		port map(
			rst        => p_Reset,
			wr_clk     => p_Clock,
			rd_clk     => p_ReadClock,
			din        => s_RxData,
			wr_en      => s_RxWrite,
			rd_en      => p_RxRead,
			dout       => o_RxData,
			full       => s_RxFull,
			wr_ack     => s_RxWriteAck,
			empty      => s_RxEmpty,
			prog_empty => s_RxProgEmpty
		);

	read_rx : process(p_Clock, p_Reset) is
	begin
		if p_Reset = '1' then
			s_State    <= Idle;
			s_RxCount  <= 0;
			s_RxData   <= (others => '0');
			s_RxIndex  <= 0;
			s_RxSample <= (others => '0');
			s_RxWrite  <= '0';
		elsif rising_edge(p_Clock) then
			case s_State is
				when Idle =>
					s_RxWrite <= '0';
					if p_Rx = '0' then
						s_State <= Start;
					end if;
				when Start =>
					if s_RxCount = c_TICK_COUNT then
						s_RxCount <= 0;
						if s_Rx = '0' then
							s_State <= Data;
						else
							s_State <= Idle;
						end if;
					elsif s_RxCount = c_SAMPLE_POINT01 or s_RxCount = c_SAMPLE_POINT02 or s_RxCount = c_SAMPLE_POINT03 then
						s_RxSample <= s_RxSample(1 downto 0) & p_Rx;
						s_RxCount  <= s_RxCount + 1;
					else
						s_RxCount <= s_RxCount + 1;
					end if;
				when Data =>
					if s_RxIndex = 8 then
						s_State   <= Stop;
						s_RxCount <= 0;
						s_RxIndex <= 0;
					else
						if s_RxCount = c_TICK_COUNT then
							s_RxData   <= s_Rx & s_RxData(7 downto 1);
							s_RxSample <= (others => '0');
							s_RxCount  <= 0;
							s_RxIndex  <= s_RxIndex + 1;
						elsif s_RxCount = c_SAMPLE_POINT01 or s_RxCount = c_SAMPLE_POINT02 or s_RxCount = c_SAMPLE_POINT03 then
							s_RxSample <= s_RxSample(1 downto 0) & p_Rx;
							s_RxCount  <= s_RxCount + 1;
						else
							s_RxCount <= s_RxCount + 1;
						end if;
					end if;
				when Stop =>
					if s_RxCount = c_TICK_COUNT then
						s_RxCount <= 0;
						s_State   <= Idle;
						if s_Rx = '1' and s_RxFull = '0' then
							s_RxWrite <= '1';
						end if;
					elsif s_RxCount = c_SAMPLE_POINT01 or s_RxCount = c_SAMPLE_POINT02 or s_RxCount = c_SAMPLE_POINT03 then
						s_RxSample <= s_RxSample(1 downto 0) & p_Rx;
						s_RxCount  <= s_RxCount + 1;
					else
						s_RxCount <= s_RxCount + 1;
					end if;
			end case;
		end if;
	end process;

	sample : process(p_Clock, p_Reset) is
	begin
		if p_Reset = '1' then
			s_Rx <= '0';
		elsif rising_edge(p_Clock) then
			case s_RxSample is
				when "000"  => s_Rx <= '0';
				when "001"  => s_Rx <= '0';
				when "010"  => s_Rx <= '0';
				when "011"  => s_Rx <= '1';
				when "100"  => s_Rx <= '0';
				when "101"  => s_Rx <= '1';
				when "110"  => s_Rx <= '1';
				when "111"  => s_Rx <= '1';
				when others => s_Rx <= '0';
			end case;

		end if;
	end process sample;

end Behavioral;
