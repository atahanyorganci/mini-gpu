----------------------------------------------------------------------------------
-- Engineer: Atahan Yorganci
-- Create Date: 02.09.2019
-- Module Name: Parser - Behavioral
-- Project Name: Mini GPU
-- Target Devices: BASYS 3
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity parser is
	Port(
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
end parser;

architecture Behavioral of parser is

	type State is (StandBy, Pulse8, Read8, Write8, Pulse16, Read16, Write16, Delay);

	constant zero16 : std_logic_vector(15 downto 0) := (others => '0');

	signal s_State  : State;
	signal s_RxRead : std_logic;

	signal s_ConfigAddr     : std_logic_vector(2 downto 0);
	signal s_ConfigAddrBuff : std_logic_vector(2 downto 0);
	signal s_ConfigBit      : std_logic;
	signal s_ConfigData     : std_logic_vector(15 downto 0);
	signal s_ConfigDataBuff : std_logic_vector(7 downto 0);
	signal s_ConfigDone     : std_logic;
	signal s_ConfigEn       : std_logic_vector(0 downto 0);
	signal s_ConfigSelect   : std_logic_vector(1 downto 0);

begin

	o_RxRead       <= s_RxRead;
	o_ConfigSelect <= s_ConfigSelect;
	o_ConfigEn     <= s_ConfigEn;
	o_ConfigAddr   <= s_ConfigAddrBuff;
	o_ConfigData   <= s_ConfigData;
	o_ConfigDone   <= s_ConfigDone;

	parse : process(p_Clock, p_Reset) is
	begin
		if p_Reset = '1' then
			s_State          <= StandBy;
			s_RxRead         <= '0';
			s_ConfigAddr     <= (others => '0');
			s_ConfigAddrBuff <= (others => '0');
			s_configBit      <= '0';
			s_ConfigData     <= (others => '0');
			s_ConfigDataBuff <= (others => '0');
			s_ConfigDone     <= '0';
			s_ConfigEn       <= "0";
			s_ConfigSelect   <= (others => '0');
		elsif rising_edge(p_Clock) then
			case s_State is
				when StandBy =>
					s_ConfigAddr     <= (others => '0');
					s_ConfigAddrBuff <= (others => '0');
					s_ConfigData     <= (others => '0');
					s_ConfigDataBuff <= (others => '0');
					s_ConfigDone     <= '0';
					s_ConfigEn       <= "0";
					s_ConfigSelect   <= (others => '0');
					if p_RxReady = '1' then
						s_RxRead <= '1';
						s_State  <= Pulse8;
					end if;
				when Pulse8 =>
					s_ConfigEn <= "0";
					s_RxRead   <= '0';
					s_State    <= Read8;
				when Read8 =>
					s_State          <= Write8;
					s_ConfigAddr     <= std_logic_vector(unsigned(s_ConfigAddr) + 1);
					s_ConfigAddrBuff <= s_ConfigAddr;
					if s_ConfigAddr = "000" then
						s_ConfigSelect <= p_RxData(2 downto 1);
						s_ConfigData   <= zero16(15 downto 1) & p_RxData(0);
					else
						s_ConfigData <= zero16(15 downto 4) & p_RxData(3 downto 0);
					end if;
				when Write8 =>
					s_ConfigEn <= "1";
					s_RxRead   <= '1';
					if s_ConfigAddrBuff = "011" then
						s_State <= Pulse16;
					else
						s_State <= Pulse8;
					end if;
				when Pulse16 =>
					s_ConfigEn <= "0";
					s_RxRead   <= '0';
					s_State    <= Read16;
				when Read16 =>
					if s_ConfigBit = '1' then
						s_ConfigAddr     <= std_logic_vector(unsigned(s_ConfigAddr) + 1);
						s_ConfigAddrBuff <= s_ConfigAddr;
						s_ConfigData     <= p_RxData & s_ConfigDataBuff;
						s_ConfigBit      <= '0';
						s_State          <= Write16;
					else
						s_ConfigBit      <= '1';
						s_ConfigDataBuff <= p_RxData;
						s_RxRead         <= '1';
						s_State          <= Pulse16;
					end if;
				when Write16 =>
					s_ConfigEn <= "1";
					if s_ConfigAddrBuff = "111" then
						s_State <= Delay;
					else
						s_RxRead <= '1';
						s_State  <= Pulse16;
					end if;
				when Delay =>
					s_ConfigDone <= '1';
					s_ConfigEn <= "0";
					s_State      <= StandBy;
			end case;
		end if;
	end process parse;

end Behavioral;
