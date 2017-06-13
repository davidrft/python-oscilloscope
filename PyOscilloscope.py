import usbtmc
import numpy as np
import matplotlib.pyplot as plt

def list_devices():
    """List all usbtmc compatible devices connected to PC."""
    if not usbtmc.list_resources():
        print("No device found.")
    else:
        for i in usbtmc.list_resources():
            inst = usbtmc.Instrument(i)
            print(inst.ask("*IDN?"))


class Osc(usbtmc.Instrument):
    
    class Generator():
        
    class Channel():
    
    class Trigger():
    
    def __init__(self, pos = 0):
        """Initializes a new device.

        Args:
        pos -- device position in devices list (provided by list_devices())
        """
        super(Osc, self).__init__(usbtmc.list_resources()[pos])
        self.write(":WAV:FORM BYTE")
        self.write(":WAV:POIN:MODE MAX")
            
    def reset(self):
        """Resets device."""
        self.write(":RST")
    
    def stop(self):
        """Stops acquisition and shows the last capture."""
        self.write(":STOP")
    
    def run(self):
        """Resumes device."""
        self.write(":RUN")
    
    def single(self):
        """Acquire a single waveform and then stops."""
        self.write(":SINGLE")
        
    def get_time_scale(self):
        """Returns current time scale."""
        return float(self.ask(":TIM:SCAL?"))
    
    def set_time_scale(self, scale):
        """Returns current time scale."""
        self.write(":TIM:SCAL {}".format(scale))
        
    def get_time_pos(self):
        """Returns current time delay."""
        return float(self.ask(":TIM:POS?"))

    def get_volt_scale(self, channel):
        """Returns current voltage scale of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.ask(":CHAN{}:SCAL?".format(channel)))
        
    def get_volt_offset(self, channel):
        """Returns current voltage offset of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.ask(":CHAN{}:OFFS?".format(channel)))
    
    def get_vpp(self, channel):
        """Returns peak-to-peak measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.ask(":MEAS:VPP? CHAN{}".format(channel)))
    
    def get_vrms(self, channel):
        """Returns rms measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.ask(":MEAS:VRMS? CHAN{}".format(channel)))
    
    def get_frequency(self, channel):
        """Returns frequency measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.ask(":MEAS:FREQ? CHAN{}".format(channel)))
    
    def get_period(self, channel):
        """Returns period measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.ask(":MEAS:PER? CHAN{}".format(channel)))

    def set_volt_scale(self, channel, scale):
        """Sets voltage scale of the selected channel to chosen value.

        Args:
        channel -- selected channel
        scale -- value to set
        """
        self.write(":CHAN{}:SCAL {}".format(channel, scale))

    def set_volt_offset(self, channel, offset):
        """Sets voltage offset of the selected channel to chosen value.

        Args:
        channel -- selected channel
        offset -- value to set
        """
        self.write(":CHAN{}:OFFS {}".format(channel, offset))
        
    def set_coupling(self, channel, mode):
        """Sets coupling mode of the selected channel to chosen value.

        Args:
        channel -- selected channel
        mode -- "AC" or "DC"
        """
        self.write(":CHAN{}:COUP {}".format(channel, mode))
    
    def gen_sin(self, amp, freq, offs=0.0):
        """Generates a sinoidal wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        offs -- wave offset (default 0.0)
        """
        self.gen_on()
        self.write("WGEN:FUNC SIN;FREQ {};VOLT {};VOLT:OFFS {}"
                   .format(freq, amp, offs))

    def gen_sqr(self, amp, freq, duty_cicle=50.0, offs=0.0):
        """Generates a square wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        duty_cycle -- wave duty_cicle (default 50.0)
        offs -- wave offset (default 0.0)
        """
        self.gen_on()
        self.write("WGEN:FUNC SQU;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:SQU:DCYC {}"
                   .format(freq, amp, offs, duty_cicle))
        
    def gen_ramp(self, amp, freq, symmetry=50.0, offs=0.0):
        """Generates a ramp wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        duty_cycle -- wave symmetry (default 50.0)
        offs -- wave offset (default 0.0)
        """
        self.gen_on()
        self.write("WGEN:FUNC RAMP;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:RAMP:SYMM {}"
                   .format(freq, amp, offs, symmetry))
    
    def gen_pulse(self, amp, freq, width, offs=0.0):
        """Generates a pulse wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        width -- pulse width
        offs -- wave offset (default 0.0)
        """
        self.gen_on()
        self.write("WGEN:FUNC PULS;FREQ {};VOLT:HIGH {};VOLT:LOW {};:WGEN:FUNC:PULS:WIDT {}"
                   .format(freq, amp, offs, width))

    def gen_dc(self, amp):
        """Generates a DC voltage.

        Args:
        amp -- wave amplitude
        """
        self.gen_on()
        self.write("WGEN:FUNC DC;VOLT:OFFS {}".format(amp))
        
    def gen_noise(self, amp, offs=0.0):
        """Generates noise.

        Args:
        amp -- noise amplitude
        offs -- noise offset (default 0.0)
        """
        self.write("WGEN:FUNC NOIS;VOLT {};VOLT:OFFS {}".format(amp, offs))
    
    def gen_on(self):
        #Turns Wave Generator on.
        self.write("WGEN:OUTP ON")
        
    def gen_off(self):
        #Turns Wave Generator off.
        self.write("WGEN:OUTP OFF")
                            
    def toggle_channel(self, channel):
        """Toggles selected channel status.

        Args:
        channel -- selected channel
        """
        status = self.ask("CHAN{}:DISP?".format(channel)) == "1"
        if status:
            self.write("CHAN{}:DISP OFF".format(channel))
        else:
            self.write("CHAN{}:DISP ON".format(channel))
    
    def get_data(self, channel, points=1000):
        """Returns wave data from selected channel as a numpy array.

        Args:
        channel -- selected channel
        """
        self.write(":DIG CHAN{}".format(channel))
        self.write(":WAV:POIN {}".format(points))
        self.write(":WAV:SOURCE CHAN{}".format(channel))
        #colocar digitize
        self.write(":WAV:DATA?")
        rawdata = self.read_raw()
        data = np.frombuffer(rawdata[10:-1], 'B')
        
        yorigin = float(self.ask(":WAV:YOR?"))
        yref = float(self.ask(":WAV:YREF?"))
        yinc = float(self.ask(":WAV:YINC?"))
        
        xorigin = float(self.ask(":WAV:XOR?"))
        xref = float(self.ask(":WAV:XREF?"))
        xinc = float(self.ask(":WAV:XINC?"))

        data_y = ((data - yref) * yinc) + yorigin
        data_x = np.array(range(len(data)))
        data_x = ((data_x - xref)) * xinc + xorigin
        
        return data_x, data_y
            
    def show_img(self, channel=1):
        """Prints acquired waveform from selected channel on PC.

        Args:
        channel -- selected channel (default 1)
        """
        self.stop()
        time, data = self.get_data(channel)
        self.run()
        
        if (time[-1] < 1e-3):
            time = time * 1e6
            t_unit = "uS"
        elif (time[-1] < 1):
            time = time * 1e3
            t_unit = "mS"
        else:
            t_unit = "S"
        
        voltscale = self.get_volt_scale(channel)
        voltoffs = self.get_volt_offset(channel)
        
        plt.plot(time, data)
        plt.title("Oscilloscope Channel {}".format(channel))
        plt.ylabel("Voltage (V)")
        plt.xlabel("Time ({})".format(t_unit))
        plt.xlim(time[0], time[-1])
        plt.ylim(-4*voltscale, 4*voltscale)
        plt.show()

x = Osc()
