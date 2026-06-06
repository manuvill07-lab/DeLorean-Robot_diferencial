#include <Arduino.h>
#include <WiFi.h>

//Inicializar sensor ultrasonico
const int trigPin = 5;
const int echoPin = 18;

//Motor izquierdo
const int leftmotor_1 = 32;
const int leftmotor_2 = 33; 

//Motor derecho
const int rightmotor_1 = 25;
const int rightmotor_2 = 26;

void detener();
void retroceder();
void girar_izquierda();
void girar_derecha();
void avanzar();

//Dentro del parentesis se pone el mismo puerto del topico publicador
WiFiServer server(8080);

void setup() {
  Serial.begin(115200);
  
  WiFi.begin("Wasabi", "Atehortua"); // Se reemplaza con el nombre de la red WiFi y la contraseña

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(leftmotor_1, OUTPUT);
  pinMode(leftmotor_2, OUTPUT);
  pinMode(rightmotor_1, OUTPUT);
  pinMode(rightmotor_2, OUTPUT);

  detener(); //Detenemos el robot al iniciar el programa

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());
  server.begin(); 
}

void loop() {
  WiFiClient client = server.available(); // Espera a que un cliente se conecte

  if (!client.connected()) {
    client = server.available();
  }

  if (client) {
    Serial.println("Cliente conectado");

    // Variable para controlar cada cuánto enviamos datos del sensor sin usar delay
    unsigned long tiempoAnterior = 0; 
    const long intervaloEnvio = 100; // Enviar datos cada 100 milisegundos

    while (client.connected()) {

      unsigned long tiempoActual = millis();

      // 1. LEER SENSOR Y ENVIAR DATOS CADA 100ms (No bloqueante)
      if (tiempoActual - tiempoAnterior >= intervaloEnvio) {
        tiempoAnterior = tiempoActual;

        long duracion, distancia;

        //Asegurar que el pin de disparo esté apagado
        digitalWrite(trigPin, LOW);
        delayMicroseconds(2);

        //Enviar el pulso ultrasónico
        digitalWrite(trigPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(trigPin, LOW);

        // Se agrega un Timeout de 30000 microsegundos para que el ESP32 no se congele
        duracion = pulseIn(echoPin, HIGH, 20000); 
        
        if (duracion == 0) {
          distancia = 500; // Si no recibe nada, asumimos que no hay obstáculo (5 metros)
        } else {
          distancia = duracion / 58.3; // Convertir a centímetros
        }

        // Enviamos al cliente (el script de ROS2/Python)
        client.println(distancia); 
      }

      // 2. RECIBIR COMANDOS Y VACIAR BUFFER PARA EVITAR LAG
      if (client.available()) {
        String data = client.readStringUntil('\n');
        data.trim();

        if (data.length() > 0) {
          Serial.print("Joystick Recibido: ");
          Serial.println(data);

          // EXTRAEMOS LA PRIMERA LETRA
          char comando = data.charAt(0);         
          
          switch (comando){
            case 'A': 
              avanzar();
              break;

            case 'R': 
              retroceder();
              break;

            case 'I': 
              girar_izquierda();
              break;

            case 'D':
              girar_derecha();
              break;

            case 'O':
            case 'F':
              detener(); 
              break;
              
            default:
              break;
          }
        }
      }
    }

    detener(); // Detenemos el robot al desconectar el cliente
    client.stop();
    Serial.println("Cliente desconectado");
  }  
}


void detener(){
  digitalWrite(leftmotor_1, LOW);
  digitalWrite(leftmotor_2, LOW);
  digitalWrite(rightmotor_1, LOW);
  digitalWrite(rightmotor_2, LOW);
}

void retroceder(){
  digitalWrite(leftmotor_1, HIGH);
  digitalWrite(leftmotor_2, LOW);
  digitalWrite(rightmotor_1, HIGH);
  digitalWrite(rightmotor_2, LOW);
}

void girar_izquierda(){
  digitalWrite(leftmotor_1, HIGH);
  digitalWrite(leftmotor_2, LOW);
  digitalWrite(rightmotor_1, LOW);
  digitalWrite(rightmotor_2, HIGH);
}

void girar_derecha(){
  digitalWrite(leftmotor_1, LOW);
  digitalWrite(leftmotor_2, HIGH);
  digitalWrite(rightmotor_1, HIGH);
  digitalWrite(rightmotor_2, LOW);
}

void avanzar(){
  digitalWrite(leftmotor_1, LOW);
  digitalWrite(leftmotor_2, HIGH);
  digitalWrite(rightmotor_1, LOW);
  digitalWrite(rightmotor_2, HIGH);
}