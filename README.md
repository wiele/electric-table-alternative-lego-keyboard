# electric-table-alternative-lego-keyboard

rpi gpio no:	co:
-----------------------------------------------------------------------------------------------
0-4				sterowanie przyciskami fabrycznymi (rpi -> switch board -> przyciski fabryczne)
5-10			przyciski lego UP, DOWN, STOP, 1, 2, 3 (przyciski lego -> rpi)


pin no		rpi func    kolor kabelka		s.b. in		s.b. out	kostki		fabr. przyc.	przyc. lego		kable alarm.
-----------------------------------------------------------------------------------------------------------------------------
2			5.0 VDC		czerwony			VCC
6			Ground		szary				GND
11			gpio 0		bordowy				IN1			przek. 1	1-2			UP								k.1. czerwony, zielony
12			gpio 1		niebieski			IN2			przek. 2	3-4			DOWN							k.1. biały, brązowy
13			gpio 2		pomaranczowy		IN3			przek. 3	5-6			1								k.1. niebieski, żółty
15			gpio 3		zielony				IN4			przek. 4	7-8			2								k.2. niebieski, brązowy
16			gpio 4		zolty				IN5			przek. 5	9-10		3								k.2. zielony, czerwony
18			gpio 5		biały										11							UP				k.2. zółty
22			gpio 6		czarny										12							DOWN			k.2. biały
7			gpio 7		czerwony									13							STOP			k.3. brązowy
3			gpio 8		niebieski									14							1				k.3. biały
5			gpio 9		zielony										15							2				k.3. zielony
24			gpio 10		żółty										16							3				k.3. czerwony
9			Ground		czarny										17							GND				k.3. niebieski
---------------------------
rpi = raspberry pi
s.b. = [relay] switch board
fabr. = fabryczne
przyc. = przyciski
