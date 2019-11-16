import enum


class EnumResource(enum.Enum):
    STONE = 2
    FOOD = 0
    WOOD = 1
    GOLD = 3
    POPULATION_HEADROOM = 4
    POPULATION = 11
    BONUS_POPULATION = 32

# TODO
# <simple id="4" name="Population Headroom" />
# <simple id="5" name="Conversion Range (Unused)" />
# <simple id="6" name="Current Age" />
# <simple id="7" name="Relics Captured" />
# <simple id="8" name="Trade Bonus (Unused?)" />
# <simple id="9" name="Trade Goods (Unused?)" />
# <simple id="10" name="Trade Production Rate (Unused?)" />
# <simple id="11" name="Population (Current and Headroom)" />
# <simple id="12" name="Corpse Decay Time (Unused?)" />
# <simple id="13" name="Discovery (Unused?)" />
# <simple id="14" name="Monuments/Ruins Captured" />
# <simple id="15" name="Animal Food (Unused)" />
# <simple id="16" name="Berries Food (Unused)" />
# <simple id="17" name="Fish Storage" />
# <simple id="18" name="Unknown" />
# <simple id="19" name="Total Units Created" />
# <simple id="20" name="Units Killed" />
# <simple id="21" name="Research Count" />
# <simple id="22" name="% Map Explored" />
# <simple id="23" name="Castle Age?" />
# <simple id="24" name="Imperial Age?" />
# <simple id="25" name="Feudal Age?" />
# <simple id="26" name="Unknown" />
# <simple id="27" name="Atonement" />
# <simple id="28" name="Redemption" />
# <simple id="29" name="Unknown" />
# <simple id="30" name="Building Limit" />
# <simple id="31" name="Food Limit" />
# <simple id="32" name="Bonus Population" />
# <simple id="33" name="Maintenance (Unused?)" />
# <simple id="34" name="Faith (Unused?)" />
# <simple id="35" name="Faith Recharging Rate" />
# <simple id="36" name="Farm Food Amount" />
# <simple id="37" name="Civilian Units (Villager High)" />
# <simple id="38" name="Unknown" />
# <simple id="39" name="All Techs Achieved" />
# <simple id="40" name="Military Units (Largest Army)" />
# <simple id="41" name="Units and Buildings Converted" />
# <simple id="42" name="Standing Wonders" />
# <simple id="43" name="Buildings Razed" />
# <simple id="44" name="Kill Ratio" />
# <simple id="45" name="Survival to Finish" />
# <simple id="46" name="Tribute Fee" />
# <simple id="47" name="Gold Mining Productivity" />
# <simple id="48" name="Town Center Unavailable" />
# <simple id="49" name="Gold Counter" />
# <simple id="50" name="Cartography" />
# <simple id="51" name="Houses (Unused)" />
# <simple id="52" name="Monastery Count" />
# <simple id="53" name="Tribute Sent" />
# <simple id="54" name="All Ruins Have Been Captured" />
# <simple id="55" name="All Relics Have Been Captured" />
# <simple id="56" name="Ore Storage (Unused)" />
# <simple id="57" name="Captured Units (Unused?)" />
# <simple id="58" name="Dark Age?" />
# <simple id="59" name="Trade Good Quality (Unused?)" />
# <simple id="60" name="Trade Market Level (Unused?)" />
# <simple id="61" name="Formations (Unused?)" />
# <simple id="62" name="Building Housing Rate" />
# <simple id="63" name="Gather Tax Rate" />
# <simple id="64" name="Gather Accumulator" />
# <simple id="65" name="Salvage Decay Rate" />
# <simple id="66" name="Allow Formations" />
# <simple id="67" name="Conversions" />
# <simple id="68" name="Hit Points Killed (Unused)" />
# <simple id="69" name="Killed P1" />
# <simple id="70" name="Killed P2" />
# <simple id="71" name="Killed P3" />
# <simple id="72" name="Killed P4" />
# <simple id="73" name="Killed P5" />
# <simple id="74" name="Killed P6" />
# <simple id="75" name="Killed P7" />
# <simple id="76" name="Killed P8" />
# <simple id="77" name="Conversion Resistance" />
# <simple id="78" name="Trade Fee" />
# <simple id="79" name="Stone Mining Productivity" />
# <simple id="80" name="Queued Units" />
# <simple id="81" name="Training Count" />
# <simple id="82" name="Start With Packed Town Center / Raider" />
# <simple id="83" name="Boarding Recharge Rate" />
# <simple id="84" name="Starting Villagers" />
# <simple id="85" name="Researches' Cost Multiplier" />
# <simple id="86" name="Researches' Time Multiplier" />
# <simple id="87" name="Boarding" />
# <simple id="88" name="Fish Trap Food Amount" />
# <simple id="89" name="Bonus Healing Rate" />
# <simple id="90" name="Healing Range" />
# <simple id="91" name="Bonus Starting Food" />
# <simple id="92" name="Bonus Starting Wood" />
# <simple id="93" name="Bonus Starting Stone" />
# <simple id="94" name="Bonus Starting Gold" />
# <simple id="95" name="Enable Town Center Packing / Raider Ability" />
# <simple id="96" name="Self Healing Seconds (Berserkers)" />
# <simple id="97" name="Sheep/Turkey Dominant LOS" />
# <simple id="98" name="Economy Score" />
# <simple id="99" name="Technology Score" />
# <simple id="100" name="Relic Gold (Collected)" />
# <simple id="101" name="Trade Profit" />
# <simple id="102" name="P1 Tribute" />
# <simple id="103" name="P2 Tribute" />
# <simple id="104" name="P3 Tribute" />
# <simple id="105" name="P4 Tribute" />
# <simple id="106" name="P5 Tribute" />
# <simple id="107" name="P6 Tribute" />
# <simple id="108" name="P7 Tribute" />
# <simple id="109" name="P8 Tribute" />
# <simple id="110" name="P1 Kill Score" />
# <simple id="111" name="P2 Kill Score" />
# <simple id="112" name="P3 Kill Score" />
# <simple id="113" name="P4 Kill Score" />
# <simple id="114" name="P5 Kill Score" />
# <simple id="115" name="P6 Kill Score" />
# <simple id="116" name="P7 Kill Score" />
# <simple id="117" name="P8 Kill Score" />
# <simple id="118" name="P1 Razings" />
# <simple id="119" name="P2 Razings" />
# <simple id="120" name="P3 Razings" />
# <simple id="121" name="P4 Razings" />
# <simple id="122" name="P5 Razings" />
# <simple id="123" name="P6 Razings" />
# <simple id="124" name="P7 Razings" />
# <simple id="125" name="P8 Razings" />
# <simple id="126" name="P1 Razing Score" />
# <simple id="127" name="P2 Razing Score" />
# <simple id="128" name="P3 Razing Score" />
# <simple id="129" name="P4 Razing Score" />
# <simple id="130" name="P5 Razing Score" />
# <simple id="131" name="P6 Razing Score" />
# <simple id="132" name="P7 Razing Score" />
# <simple id="133" name="P8 Razing Score" />
# <simple id="134" name="Standing Castles" />
# <simple id="135" name="Hit Points Razing (Unused)" />
# <simple id="136" name="Kills By P1" />
# <simple id="137" name="Kills By P2" />
# <simple id="138" name="Kills By P3" />
# <simple id="139" name="Kills By P4" />
# <simple id="140" name="Kills By P5" />
# <simple id="141" name="Kills By P6" />
# <simple id="142" name="Kills By P7" />
# <simple id="143" name="Kills By P8" />
# <simple id="144" name="Razings By P1" />
# <simple id="145" name="Razings By P2" />
# <simple id="146" name="Razings By P3" />
# <simple id="147" name="Razings By P4" />
# <simple id="148" name="Razings By P5" />
# <simple id="149" name="Razings By P6" />
# <simple id="150" name="Razings By P7" />
# <simple id="151" name="Razings By P8" />
# <simple id="152" name="Units Lost Score" />
# <simple id="153" name="Buildings Lost Score" />
# <simple id="154" name="Units Lost" />
# <simple id="155" name="Buildings Lost" />
# <simple id="156" name="Tribute From P1" />
# <simple id="157" name="Tribute From P2" />
# <simple id="158" name="Tribute From P3" />
# <simple id="159" name="Tribute From P4" />
# <simple id="160" name="Tribute From P5" />
# <simple id="161" name="Tribute From P6" />
# <simple id="162" name="Tribute From P7" />
# <simple id="163" name="Tribute From P8" />
# <simple id="164" name="Current Units Score" />
# <simple id="165" name="Current Buildings Score" />
# <simple id="166" name="Food Collected" />
# <simple id="167" name="Wood Collected" />
# <simple id="168" name="Stone Collected" />
# <simple id="169" name="Gold Collected" />
# <simple id="170" name="Score: Military" />
# <simple id="171" name="Tribute Received" />
# <simple id="172" name="Razing Score" />
# <simple id="173" name="Total Castles" />
# <simple id="174" name="Total Wonders" />
# <simple id="175" name="Score: Economy (Tribute)" />
# <simple id="176" name="Convert Min Adjustment" />
# <simple id="177" name="Convert Max Adjustment" />
# <simple id="178" name="Convert Resist Min Adjustment" />
# <simple id="179" name="Convert Resist Max Adjustment" />
# <simple id="180" name="Convert Building Min" />
# <simple id="181" name="Convert Building Max" />
# <simple id="182" name="Convert Building Chance" />
# <simple id="183" name="Spies" />
# <simple id="184" name="Society Score" />
# <simple id="185" name="Food Score" />
# <simple id="186" name="Wood Score" />
# <simple id="187" name="Stone Score" />
# <simple id="188" name="Gold Score" />
# <simple id="189" name="Chopping Productivity" />
# <simple id="190" name="Food-gathering Productivity" />
# <simple id="191" name="Relic Gold Production Rate" />
# <simple id="192" name="Heresy" />
# <simple id="193" name="Theocracy" />
# <simple id="194" name="Crenellations (Garrisoned Inf.)" />
# <simple id="195" name="Build Rate (Except Wonders)" />
# <simple id="196" name="Atheism (Wonder Bonus)" />
# <simple id="197" name="Atheism (Spies Discount)" />
# <simple id="198" name="Unk 198 (unused?)" />
# <simple id="199" name="Unk 199 (unused?)" />
# <simple id="200" name="Unk 200 (unused?)" />
# <simple id="201" name="Unk 201 (unused?)" />
# <simple id="202" name="Unk 202 (unused?)" />
# <simple id="203" name="Unk 203 (unused?)" />
# <simple id="204" name="Unk 204 (unused?)" />
# <simple id="205" name="Feitoria Food Productivity" />
# <simple id="206" name="Feitoria Wood Productivity" />
# <simple id="207" name="Feitoria Stone Productivity" />
# <simple id="208" name="Feitoria Gold Productivity" />
