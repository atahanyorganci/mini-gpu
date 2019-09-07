----------------------------------------------------------------------------------
-- Engineer: Atahan Yorganci
-- Create Date: 02.09.2019
-- Module Name: Bank - Behavioral
-- Project Name: Mini GPU
-- Target Devices: BASYS 3
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity bank is
	Port(
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
end bank;

architecture Behavioral of bank is

	type ColorArray is array (0 to 3) of std_logic_vector(11 downto 0);

	component rectangle
		port(
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
	end component rectangle;

	signal s_RectangleEn    : std_logic_vector(3 downto 0);
	signal s_RectangleColor : ColorArray;
	signal s_RectangleDraw  : std_logic_vector(3 downto 0);

begin

	decoder : process(p_Clock, p_Reset) is
	begin
		if p_Reset = '1' then
			s_RectangleEn <= (others => '0');
		elsif rising_edge(p_Clock) then
			case p_ConfigSelect is
				when "00"   => s_RectangleEn <= "000" & p_ConfigEn;
				when "01"   => s_RectangleEn <= "00" & p_ConfigEn & "0";
				when "10"   => s_RectangleEn <= "0" & p_ConfigEn & "00";
				when "11"   => s_RectangleEn <= p_ConfigEn & "000";
				when others => s_RectangleEn <= (others => '0');
			end case;
		end if;
	end process decoder;

	priority_decoder : process(p_Clock, p_Reset) is
	begin
		if p_Reset = '1' then
			o_Color <= (others => '0');
		elsif rising_edge(p_Clock) then
			if s_RectangleDraw(0) = '1' then
				o_Color <= s_RectangleColor(0);
			elsif s_RectangleDraw(1) = '1' then
				o_Color <= s_RectangleColor(1);
			elsif s_RectangleDraw(2) = '1' then
				o_Color <= s_RectangleColor(2);
			elsif s_RectangleDraw(3) = '1' then
				o_Color <= s_RectangleColor(3);
			else
				o_Color <= (others => '0');
			end if;
		end if;
	end process priority_decoder;

	rectangle01 : rectangle
		port map(
			p_Clock      => p_Clock,
			p_Reset      => p_Reset,
			p_HPos       => p_HPos,
			p_VPos       => p_VPos,
			p_ConfigEn   => s_RectangleEn(0 downto 0),
			p_ConfigAddr => p_ConfigAddr,
			p_ConfigData => p_ConfigData,
			p_ConfigDone => p_ConfigDone,
			o_Color      => s_RectangleColor(0),
			o_Draw       => s_RectangleDraw(0)
		);

	rectangle02 : rectangle
		port map(
			p_Clock      => p_Clock,
			p_Reset      => p_Reset,
			p_HPos       => p_HPos,
			p_VPos       => p_VPos,
			p_ConfigEn   => s_RectangleEn(1 downto 1),
			p_ConfigAddr => p_ConfigAddr,
			p_ConfigData => p_ConfigData,
			p_ConfigDone => p_ConfigDone,
			o_Color      => s_RectangleColor(1),
			o_Draw       => s_RectangleDraw(1)
		);

	rectangle03 : rectangle
		port map(
			p_Clock      => p_Clock,
			p_Reset      => p_Reset,
			p_HPos       => p_HPos,
			p_VPos       => p_VPos,
			p_ConfigEn   => s_RectangleEn(2 downto 2),
			p_ConfigAddr => p_ConfigAddr,
			p_ConfigData => p_ConfigData,
			p_ConfigDone => p_ConfigDone,
			o_Color      => s_RectangleColor(2),
			o_Draw       => s_RectangleDraw(2)
		);

	rectangle04 : rectangle
		port map(
			p_Clock      => p_Clock,
			p_Reset      => p_Reset,
			p_HPos       => p_HPos,
			p_VPos       => p_VPos,
			p_ConfigEn   => s_RectangleEn(3 downto 3),
			p_ConfigAddr => p_ConfigAddr,
			p_ConfigData => p_ConfigData,
			p_ConfigDone => p_ConfigDone,
			o_Color      => s_RectangleColor(3),
			o_Draw       => s_RectangleDraw(3)
		);
end Behavioral;
