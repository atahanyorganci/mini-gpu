----------------------------------------------------------------------------------
-- Engineer: Atahan Yorganci
-- Create Date: 29.08.2019
-- Module Name: Rectangle - Behavioral
-- Project Name: Mini GPU
-- Target Devices: BASYS 3
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity rectangle is
	Port(
		p_Clock      : in  std_logic;
		p_Reset      : in  std_logic;
		p_HPos       : in  integer range 0 to 65535;
		p_VPos       : in  integer range 0 to 65535;
		p_ConfigEn   : in  std_logic_vector(0 downto 0);
		p_ConfigAddr : in  std_logic_vector(2 downto 0);
		p_ConfigData : in  std_logic_vector(15 downto 0);
		p_ConfigDone : in  std_logic;
		o_Color      : out std_logic_vector(11 downto 0);
		o_Draw       : out std_logic
	);
end rectangle;

architecture Behavioral of rectangle is

	component rectangle_ram
		port(
			clka  : IN  STD_LOGIC;
			wea   : IN  STD_LOGIC_VECTOR(0 DOWNTO 0);
			addra : IN  STD_LOGIC_VECTOR(2 DOWNTO 0);
			dina  : IN  STD_LOGIC_VECTOR(15 DOWNTO 0);
			clkb  : IN  STD_LOGIC;
			addrb : IN  STD_LOGIC_VECTOR(2 DOWNTO 0);
			doutb : OUT STD_LOGIC_VECTOR(15 DOWNTO 0)
		);
	end component rectangle_ram;

	type State is (Idle, RC, Config, Calculate, Enable);

	-- RAM
	signal s_Address : std_logic_vector(2 downto 0);
	signal s_DataOut : std_logic_vector(15 downto 0);

	-- Rectangle Config
	signal s_State   : State;
	signal s_Enable  : std_logic;
	signal s_HCorner : integer;
	signal s_VCorner : integer;
	signal s_Width   : integer;
	signal s_Height  : integer;
	signal s_HOffset : integer;
	signal s_VOffset : integer;
	signal s_Color   : std_logic_vector(11 downto 0);
	signal s_Draw    : std_logic;

begin

	o_Color <= s_Color;
	o_Draw  <= s_Draw;

	config_ram : component rectangle_ram
		port map(
			clka  => p_Clock,
			wea   => p_ConfigEn,
			addra => p_ConfigAddr,
			dina  => p_ConfigData,
			clkb  => p_Clock,
			addrb => s_Address,
			doutb => s_DataOut
		);

	configure : process(p_Clock, p_Reset) is
	begin
		if p_Reset = '1' then
			s_Address <= (others => '0');
			s_State   <= Idle;
			s_Enable  <= '0';
			s_HCorner <= 0;
			s_VCorner <= 0;
			s_Width   <= 0;
			s_Height  <= 0;
			s_HOffset <= 0;
			s_VOffset <= 0;
			s_Color   <= (others => '0');
		elsif rising_edge(p_Clock) then
			case s_State is
				when Idle =>
					if p_ConfigDone = '1' then
						s_State   <= RC;
						s_Address <= "000";
					end if;
				when RC =>
					s_Address <= std_logic_vector(unsigned(s_Address) + 1);
					case s_Address is
						when "000" => null;
						when "001" =>
							if s_DataOut(0) = '1' then
								s_Enable <= '1';
							else
								s_Enable <= '0';
							end if;
						when "010" =>
							s_Color <= s_DataOut(3 downto 0) & s_Color(7 downto 0);
						when "011" =>
							s_Color <= s_Color(11 downto 8) & s_DataOut(3 downto 0) & s_Color(3 downto 0);
						when "100" =>
							s_Color <= s_Color(11 downto 4) & s_DataOut(3 downto 0);
						when "101" =>
							s_HCorner <= to_integer(unsigned(s_DataOut));
						when "110" =>
							s_VCorner <= to_integer(unsigned(s_DataOut));
						when "111" =>
							s_Width <= to_integer(unsigned(s_DataOut));
							s_State <= Config;
						when others =>
							s_State   <= Idle;
							s_Address <= "000";
					end case;
				when Config =>
					s_Height <= to_integer(unsigned(s_DataOut));
					s_State  <= Calculate;
				when Calculate =>
					s_HOffset <= s_HCorner + s_Width;
					s_VOffset <= s_VCorner + s_Height;
					s_State   <= Enable;
				when Enable =>
					if p_ConfigDone = '1' then
						s_State  <= RC;
						s_Enable <= '0';
					end if;
			end case;
		end if;
	end process configure;

	draw : process(p_Clock, p_Reset)
	begin
		if (p_Reset = '1') then
			s_Draw <= '0';
		elsif rising_edge(p_Clock) then
			if p_HPos >= s_HCorner and p_HPos < s_HOffset and p_VPos >= s_VCorner and p_VPos < s_VOffset and s_Enable = '1' then
				s_Draw <= '1';
			else
				s_Draw <= '0';
			end if;
		end if;
	end process;

end Behavioral;
