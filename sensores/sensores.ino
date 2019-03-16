#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <math.h>
#include <DHT.h> //Biblioteca Sensor DHT

#define DHTPIN 7

// Utilize a linha de acordo com o modelo do sensor
//#define DHTTYPE DHT11   // Sensor DHT11
#define DHTTYPE DHT22   // Sensor DHT 22  (AM2302)
//#define DHTTYPE DHT21   // Sensor DHT 21 (AM2301)
// Definicoes do sensor : pino, tipo
DHT dht(DHTPIN, DHTTYPE);


/* possibilidades/niveis de acordo com a resolução */
#define   ADC_16BIT_MAX   65536

/* cria instância do conversor analogico digital ADC */
Adafruit_ADS1115 ads(0x48);

//Declaração de variáveis 
float ads_bit_Voltage;
float I; //Define variável corrente do painel 
float V; //Define variável tensão do painel
float V1; //Define variável auxiliar para calculo da tensão do painel
float Ir; //Definel variável irradiação piranometro 
float Temp; //Definel variável irradiação piranometro

int LDR_1k = 4; //Define a variável LDR + 1k como pino A4.
int LDR_750 = 5; //Define a variável LDR + 100 como pino A5.
int LDR_470 = 3; //Define a variável LDR + 500 como pino A3.
int Corrente = 6;  //Define a variável Corrente como pino A6.
int Tensao = 7;  //Define a variável Tensao como pino A7.
int VAL11 = 0;
int VAL22 = 0;
int VAL33 = 0;
int Corrente1 = 0;
int Tensao1 = 0;
double V_1k = 0;
double V_750 = 0;
double V_470 = 0;
double Corrente2 = 0;
double Tensao2 = 0;

void setup(void) 
{
  
  Serial.begin(115200);
  while (!Serial);
  
//  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
//  ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
//  ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
//  ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
//  ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV

  /* inicializa o ADC */
  ads.begin();

  /* modifique este valor de acordo com o ganho selecionado */
  float ads_InputRange = 0.256f;
  /* no range de +-6.144V, 187.502uV/bit */
  ads_bit_Voltage = (ads_InputRange * 2) / (ADC_16BIT_MAX - 1);
  dht.begin();
}

void loop(void) 
{ 

  Serial.write("T\n");
  postDHT();
  postLDRs();
  postTenCor();
  postPiranometro();
  //postTermopar();

  delay(3000);

}

void postDHT(){
  
  // Leitura da umidade
  double h = dht.readHumidity();    
  // Leitura da temperatura (Celsius)
  double t = dht.readTemperature();
  Serial.write("a");
  Serial.write(String(String(h,2).length()).c_str());
  Serial.write(String(h,2).c_str());
  Serial.write(String(String(t,2).length()).c_str());
  Serial.write(String(t,2).c_str());
}

void postLDRs(){

  //Leitura de tensão dos LDR´s conectados das portas A3 a A7

  VAL11 = analogRead(LDR_1k);   
  V_1k = 0.0048828125*VAL11;

  Serial.write("b");
  Serial.write(String(String(V_1k,3).length()).c_str());
  Serial.write(String(V_1k,3).c_str());  
  

  VAL22 = analogRead(LDR_750);   
  V_750 = 0.0048828125*VAL22;

  Serial.write("c");
  Serial.write(String(String(V_750,3).length()).c_str());
  Serial.write(String(V_750,3).c_str());  
  

  VAL33 = analogRead(LDR_470);   
  V_470 = 0.0048828125*VAL33;

  Serial.write("d");
  Serial.write(String(String(V_470,3).length()).c_str());
  Serial.write(String(V_470,3).c_str());  
  
  
}

void postTenCor(){

  Corrente1 = analogRead(Corrente);   
  Corrente2 = 0.0048828125*Corrente1;
  I = (Corrente2 - 2.5065)/0.1;

  Tensao1 = analogRead(Tensao);   
  Tensao2 = 0.0048828125*Tensao1;
  V = (40.57/4.02)*Tensao2;
  V1 = 1.006*V-0.001387;

  Serial.write('e');
  Serial.write(String(String(I,3).length()).c_str());
  Serial.write(String(I,3).c_str());
  Serial.write(String(String(Corrente2,3).length()).c_str());
  Serial.write(String(Corrente2,3).c_str());
  Serial.write(String(String(V1,3).length()).c_str());
  Serial.write(String(V1,3).c_str());
  Serial.write(String(String(Tensao2,3).length()).c_str());
  Serial.write(String(Tensao2,3).c_str());

}

void postPiranometro(){
  int16_t ads_ch2 = 2;
  int16_t nano_ch2_0 = 0;           // usando referencia de Vcc (5V)
  int16_t nano_ch2_1 = 0;           // usando referencia interna (1.1V)
  /* variaveis para armazenar o resultado em tensao */
  float ads_Voltage_ch2 = 0.0f;
  /* variaveis apra armazenar o valor RAW do adc */

  ads_ch2 = ads.readADC_SingleEnded(2);
  
  
  if(ads_ch2>0){
    ads_Voltage_ch2 = ads_ch2 * ads_bit_Voltage;
  }
  
  
  
  
  Ir = (1000/(0.01244))*ads_Voltage_ch2;
  
  Serial.write('f'); 
  Serial.write(String(String(Ir,3).length()).c_str());
  Serial.write(String(Ir,3).c_str());
  Serial.write(String(String(ads_Voltage_ch2,4).length()).c_str());
  Serial.write(String(ads_Voltage_ch2,4).c_str());

  
}

void postTermopar(){
  int16_t ads_ch3 = 3;
  int16_t nano_ch3_0 = 0;           // usando referencia de Vcc (5V)
  int16_t nano_ch3_1 = 0;           // usando referencia interna (1.1V)
  /* variaveis para armazenar o resultado em tensao */
  float ads_Voltage_ch3 = 0.0f;
  ads_ch3 = ads.readADC_SingleEnded(3);
  ads_Voltage_ch3 = ads_ch3 * ads_bit_Voltage;
  Temp = 25707*ads_Voltage_ch3 - 567756*ads_Voltage_ch3*ads_Voltage_ch3 + 0.0339;

  Serial.write('g'); 
  Serial.write(String(String(Temp,3).length()).c_str());
  Serial.write(String(Temp,3).c_str());
  Serial.write(String(String(ads_Voltage_ch3,3).length()).c_str());
  Serial.write(String(ads_Voltage_ch3,3).c_str());
  
}
