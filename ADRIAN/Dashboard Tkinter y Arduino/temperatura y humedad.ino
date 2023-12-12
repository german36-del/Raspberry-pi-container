#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
int ledPin = 13; // El pin del LED

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(ledPin, OUTPUT); // Configura el pin del LED como salida
}

void loop() {

  if (Serial.available()) { // Si hay datos en el puerto serial
    char comando = Serial.read(); // Lee el comando
    if (comando == '1') { // Si el comando es "1"
      digitalWrite(ledPin, HIGH); // Enciende el LED
    }
    else if (comando == '0') { // Si el comando es "0"
      digitalWrite(ledPin, LOW); // Apaga el LED
    }
  }
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();
  
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print("°C");

  Serial.print(" Humedad: ");
  Serial.print(humedad);
  Serial.println("%");

  delay(1000);
}
