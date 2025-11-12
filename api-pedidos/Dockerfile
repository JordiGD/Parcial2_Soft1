FROM eclipse-temurin:21-jdk-alpine

WORKDIR /app

RUN apk add --no-cache curl maven

COPY pedidos/pom.xml .
COPY pedidos/src ./src

RUN mvn clean package -DskipTests -Dmaven.test.skip=true

EXPOSE 8080

CMD ["java", "-jar", "target/pedidos-0.0.1-SNAPSHOT.jar"]
