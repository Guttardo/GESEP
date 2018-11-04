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
  /* inicializa a serial */
  Serial.begin(9600);
  /* aguarda a serial estar disponível */
  while (!Serial);
  /* imprime o nome do arquivo com data e hora */
  //Serial.println(F("\r\n"__FILE__"\t"__DATE__" "__TIME__));
  /*
   * configura o ganho do PGA interno do ADS1115
   * - Sem configurar ele inicia automaticamente na escala de +/- 6.144V
   * - lembre-se de não exceder os limites de tensao nas entradas
   * - - VDD+0.3v ou GND-0.3v
   */
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
    /*
   * imprime o valor da tensao por bit
   * - ADS1115 (de acordo com o ganho do PGA)
   * - Arduino Nano/Uno com referencia em Vcc
   * - Arduino Nano/Uno com referencia interna de 1.1V
   */
  Serial.println();
  Serial.print("ADS volt/bit: ");   Serial.print(ads_bit_Voltage * 1000, 4);     Serial.println(" mV/bit");
  Serial.println();
  Serial.println();

  /* imprime a primeira linha com identificacao dos dados */
  Serial.println("ADS RAW \tADS Temp.");
  /* seta a referencia interna */
  //analogReference(INTERNAL);

  dht.begin();
}

void loop(void) 
{ 
  // Leitura da umidade
  float h = dht.readHumidity();
  // Leitura da temperatura (Celsius)
  float t = dht.readTemperature();
  
  // Verifica se o sensor DHT22 esta comunicando corretamente
  if (isnan(h) || isnan(t))
  {
    Serial.println("Falha ao ler dados do sensor DHT !!!");
    return;
  }

  // Mostra a temperatura ambiente no serial monitor 
  Serial.print("Temperatura Ambiente: "); 
  Serial.print(t);
  Serial.println(" *C  ");
  Serial.println();
  // Mostra a umidade no serial monitor 
  Serial.print("Umidade : "); 
  Serial.print(h);
  Serial.println(" %");
  Serial.println();
 
  //Leitura de tensão dos LDR´s conectados das portas A3 a A7
  VAL11 = analogRead(LDR_1k);   
  V_1k = 0.0048828125*VAL11;
  
  VAL22 = analogRead(LDR_750);   
  V_750 = 0.0048828125*VAL22;
  
  VAL33 = analogRead(LDR_470);   
  V_470 = 0.0048828125*VAL33;
  
  Corrente1 = analogRead(Corrente);   
  Corrente2 = 0.0048828125*Corrente1;
  I = (Corrente2 - 2.5065)/0.1;
  
  Tensao1 = analogRead(Tensao);   
  Tensao2 = 0.0048828125*Tensao1;
  V = (40.57/4.02)*Tensao2;
  V1 = 1.006*V-0.001387;
  
  //Mostra as tensões dos LDR´s no serial monitor
  Serial.print("Tensao LDR_470 = ");
  Serial.print(V_470);
  Serial.println(" V  ");
  
  Serial.print("Tensao LDR_750 = ");
  Serial.print(V_750);
  Serial.println(" V  ");
  
  Serial.print("Tensao LDR_1k = ");
  Serial.print(V_1k);
  Serial.println(" V  ");
  Serial.println();
  
  Serial.print("Corrente Painel = ");
  Serial.print(I);
  Serial.print(" A  "); Serial.print("\t\t");
  Serial.print("Sensor Corrente = ");
  Serial.print(Corrente2, 3);       
  Serial.println(" V"); 
  
  Serial.print("Tensao Painel = ");
  Serial.print(V1);
  Serial.print(" V  "); Serial.print("\t\t");
  Serial.print("Sensor Tensao = ");
  Serial.print(Tensao2, 3);       
  Serial.println(" V"); 
  
  Serial.println();

  //Codigo para leitura das variaveis conectadas ao ADS1115
   /* variaveis apra armazenar o valor RAW do adc */
  //int16_t ads_ch0 = 0;
  //int16_t nano_ch0_0 = 0;           // usando referencia de Vcc (5V)
  //int16_t nano_ch0_1 = 0;           // usando referencia interna (1.1V)
  /* variaveis para armazenar o resultado em tensao */
  //float ads_Voltage_ch0 = 0.0f;
  /* variaveis para armazenar a temperatura */
  //float ads_Temperature_ch0 = 0.0f;

  /* variaveis apra armazenar o valor RAW do adc */
  //int16_t ads_ch1 = 1;
  //int16_t nano_ch1_0 = 0;           // usando referencia de Vcc (5V)
  //int16_t nano_ch1_1 = 0;           // usando referencia interna (1.1V)
  /* variaveis para armazenar o resultado em tensao */
  //float ads_Voltage_ch1 = 0.0f;

  /* variaveis apra armazenar o valor RAW do adc */
  int16_t ads_ch2 = 2;
  int16_t nano_ch2_0 = 0;           // usando referencia de Vcc (5V)
  int16_t nano_ch2_1 = 0;           // usando referencia interna (1.1V)
  /* variaveis para armazenar o resultado em tensao */
  float ads_Voltage_ch2 = 0.0f;

  /* variaveis apra armazenar o valor RAW do adc */
  int16_t ads_ch3 = 3;
  int16_t nano_ch3_0 = 0;           // usando referencia de Vcc (5V)
  int16_t nano_ch3_1 = 0;           // usando referencia interna (1.1V)
  /* variaveis para armazenar o resultado em tensao */
  float ads_Voltage_ch3 = 0.0f;
  
  /********************************************
   * ADS1115 - 16bit ADC
   * - le o ADC
   * - converter o valor RAW em tensao
   * - calcula a temperatura
   ********************************************/
  // Porta A0 ADS1115 - Corrente do painel
  //ads_ch0 = ads.readADC_SingleEnded(0);
  //ads_Voltage_ch0 = ads_ch0 * ads_bit_Voltage;
  //I = (ads_Voltage_ch0 - 2.5065)/0.1;
  /* imprime os resultados */
  //Serial.print("Corrente Painel = ");
  //Serial.print(I, 3);       
  //Serial.print(" A"); Serial.print("\t\t");
  //Serial.print("Tensao Sensor Corrente = ");
  //Serial.print(ads_Voltage_ch0, 3);       
  //Serial.println(" V"); Serial.print("\t\t"); 
  //Serial.println();
  
  // Porta A1 ADS1115 - Tensão do painel
  //ads_ch1 = ads.readADC_SingleEnded(1);
  //ads_Voltage_ch1 = ads_ch1 * ads_bit_Voltage;
  //V = (40.57/4.02)*ads_Voltage_ch1;
  //V1 = 1.006*V-0.001387;
  /* imprime os resultados */
  //Serial.print("Tensao Painel = ");
  //Serial.print(V1, 3);       
  //Serial.print(" V"); Serial.print("\t\t");
  //Serial.print("Sensor Tensao = ");
  //Serial.print(ads_Voltage_ch1, 3);       
  //Serial.println(" V"); Serial.print("\t\t"); 
  Serial.println();
  
  // Porta A2 ADS1115 - Piranometro 
  ads_ch2 = ads.readADC_SingleEnded(2);
  ads_Voltage_ch2 = ads_ch2 * ads_bit_Voltage;
  Ir = (1000/(0.01244))*ads_Voltage_ch2;
  /* imprime os resultados */
  Serial.print("Irradiacao Piranometro = ");
  Serial.print(Ir, 3);       
  Serial.print(" W/m2"); Serial.print("\t\t");
  Serial.print("Tensao Piranometro = ");
  Serial.print(ads_Voltage_ch2, 3);       
  Serial.println(" V"); Serial.print("\t\t"); 
  Serial.println();

  // Porta A3 ADS1115 - Termopar Tipo T 
  ads_ch3 = ads.readADC_SingleEnded(3);
  ads_Voltage_ch3 = ads_ch3 * ads_bit_Voltage;
  //Temp = 0.0002*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3 - 0.0056*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3 + 0.0401*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3 - 0.089*ads_Voltage_ch3*ads_Voltage_ch3*ads_Voltage_ch3 - 0.5586*ads_Voltage_ch3*ads_Voltage_ch3 + 25.82*ads_Voltage_ch3 - 0.0081;
  Temp = 25707*ads_Voltage_ch3 - 567756*ads_Voltage_ch3*ads_Voltage_ch3 + 0.0339;
  /* imprime os resultados */
  Serial.print("Temperatura Termopar = ");
  Serial.print(Temp, 3);       
  Serial.print(" *C"); Serial.print("\t\t");
  Serial.print("Tensao Piranometro = ");
  Serial.print(ads_Voltage_ch3, 3);       
  Serial.println(" V"); Serial.print("\t\t"); 
  Serial.println();
 

  Serial.println("_______________________________________________________________________________________");
  Serial.println();

  delay(2000);
}
