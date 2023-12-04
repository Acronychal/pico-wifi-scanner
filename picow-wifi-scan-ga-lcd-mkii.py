import network
from machine import Pin,SPI,PWM
import framebuf
import time

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch8(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 160
        self.height = 128
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        

        self.WHITE = 0xFFFFFF
        self.RED = 0xFF0000
        self.GREEN = 0x00FF00
        self.BLUE = 0x0000FF
        self.YELLOW = 0xFFFF00
        self.CYAN = 0x00FFFF
        self.MAGENTA = 0xFF00FF
        self.BLACK = 0x000000
        self.GRAY = 0x808080
        self.SILVER = 0xC0C0C0
        self.MAROON = 0x800000
        self.OLIVE = 0x808000
        self.NAVY = 0x000080
        self.PURPLE = 0x800080
        self.TEAL = 0x008080
        self.ORANGE = 0xFFA500
        self.LIME = 0x00FF00
        self.PINK = 0xFFC0CB
        self.BROWN = 0xA52A2A
        self.INDIGO = 0x4B0082


        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36);
        self.write_data(0x70);
        
        self.write_cmd(0x3A);
        self.write_data(0x05);

         #ST7735R Frame Rate
        self.write_cmd(0xB1);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB2);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB3);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB4); #Column inversion
        self.write_data(0x07);

        #ST7735R Power Sequence
        self.write_cmd(0xC0);
        self.write_data(0xA2);
        self.write_data(0x02);
        self.write_data(0x84);
        self.write_cmd(0xC1);
        self.write_data(0xC5);

        self.write_cmd(0xC2);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0xC3);
        self.write_data(0x8A);
        self.write_data(0x2A);
        self.write_cmd(0xC4);
        self.write_data(0x8A);
        self.write_data(0xEE);

        self.write_cmd(0xC5); #VCOM
        self.write_data(0x0E);

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0);
        self.write_data(0x0f);
        self.write_data(0x1a);
        self.write_data(0x0f);
        self.write_data(0x18);
        self.write_data(0x2f);
        self.write_data(0x28);
        self.write_data(0x20);
        self.write_data(0x22);
        self.write_data(0x1f);
        self.write_data(0x1b);
        self.write_data(0x23);
        self.write_data(0x37);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x02);
        self.write_data(0x10);

        self.write_cmd(0xe1);
        self.write_data(0x0f);
        self.write_data(0x1b);
        self.write_data(0x0f);
        self.write_data(0x17);
        self.write_data(0x33);
        self.write_data(0x2c);
        self.write_data(0x29);
        self.write_data(0x2e);
        self.write_data(0x30);
        self.write_data(0x30);
        self.write_data(0x39);
        self.write_data(0x3f);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x03);
        self.write_data(0x10);

        self.write_cmd(0xF0); #Enable test command
        self.write_data(0x01);

        self.write_cmd(0xF6); #Disable ram power save mode
        self.write_data(0x00);

            #sleep out
        self.write_cmd(0x11);
        #DEV_Delay_ms(120);

        #Turn on the LCD display
        self.write_cmd(0x29);

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xA0)
        
        
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x81)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    def set_orientation(self, orientation):
        # Set MADCTL (Memory Access Control) register to control display orientation
        self.write_cmd(0x36)
        if orientation == 0:
            self.write_data(0xA0)
        elif orientation == 1:
            self.write_data(0x60)
        elif orientation == 2:
            self.write_data(0xC0)
        elif orientation == 3:
            self.write_data(0x00)
        else:
            raise ValueError("Invalid orientation value. Use 0, 1, 2, or 3.")        
        
        
  
def show_splash_screen(LCD):
    # Draw a filled rectangle as the background
    LCD.fill_rect(0, 0, LCD.width, LCD.height, LCD.BLACK)

    # Draw a border around the screen
    LCD.rect(0, 0, LCD.width, LCD.height, LCD.WHITE)

    # Display splash screen content
    #LCD.text("Welcome to", 20, 40, LCD.WHITE)
    LCD.text("RPI Pico W Scanner", 5, 60, LCD.WHITE)

    # Draw a separator line
    #LCD.hline(0, 80, LCD.width, LCD.WHITE)

    LCD.show()
    time.sleep(2)  # Adjust the duration the splash screen is displayed
  
      
   
      
      
      


def print_network_info_to_lcd(LCD, scan_results, channel):
    LCD.fill(LCD.BLACK)
    LCD.text(f"Ch {channel:<2} | {'SSID':<4} | {'-db':<5}", 6, 5, LCD.WHITE)


    # Display scan results in a table format
    y_position = 20  # Initial y position for displaying networks
    for result in scan_results:
        ssid = result[0].decode('utf-8')[:12]
        bssid = ':'.join('{:02x}'.format(b) for b in result[1])
        rssi = result[3]

        network_info = f"{ssid:<12} | {rssi:3d}"

        LCD.text(network_info, 6, y_position, LCD.BLUE)
        y_position += 10  # Increase y position for the next network

    LCD.show()

def main():
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)  # max 65535

    LCD = LCD_1inch8()
    LCD.fill(LCD.BLACK)
    LCD.set_orientation(0)
    show_splash_screen(LCD)
    
    LCD.show()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    time.sleep(2)  # Give some time for the scan to complete

    channels_to_scan = range(1, 14)  # Channels 1 to 13

    for channel in channels_to_scan:
        wlan.active(False)
        wlan.config(channel=channel)
        wlan.active(True)

        time.sleep(1)  # Wait for some time to stabilize
        scan_results = wlan.scan()
        
        

        # Print to serial
        print(f"\nNetworks on Channel {channel}:\n")
        for result in scan_results:
            ssid = result[0].decode('utf-8')[:30]
            bssid = ':'.join('{:02x}'.format(b) for b in result[1])
            rssi = result[3]
            print(f"SSID: {ssid:<30} | RSSI: {rssi:3d} | BSSID: {bssid:<10}")

        # Display on LCD
        print_network_info_to_lcd(LCD, scan_results, channel)

        time.sleep(2)  # Optional delay before moving to the next channel
        #LCD.fill(LCD.BLACK)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)