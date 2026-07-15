package com.poweresfot.examen;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class DatosController {

    private final JdbcTemplate jdbcTemplate;

    @Value("${server.name:servidor-desconocido}")
    private String serverName;

    public DatosController(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    /*
     * Devuelve los registros en formato:
     * usuario,accion,fecha,hora,video
     */
    @GetMapping(
            value = "/datos",
            produces = MediaType.TEXT_PLAIN_VALUE
    )
    public ResponseEntity<String> obtenerDatos() {

        String sql = """
                SELECT
                    usuario,
                    accion,
                    DATE_FORMAT(fecha, '%Y-%m-%d') AS fecha,
                    TIME_FORMAT(hora, '%H:%i:%s') AS hora,
                    short
                FROM redes
                ORDER BY id
                """;

        List<String> registros = jdbcTemplate.query(
                sql,
                (resultado, numeroFila) ->
                        resultado.getString("usuario") + "," +
                        resultado.getString("accion") + "," +
                        resultado.getString("fecha") + "," +
                        resultado.getString("hora") + "," +
                        resultado.getString("short")
        );

        String contenido = String.join("\n", registros);

        HttpHeaders encabezados = new HttpHeaders();
        encabezados.add("X-Server-Name", serverName);
        encabezados.add("X-Total-Registros", String.valueOf(registros.size()));

        return ResponseEntity
                .ok()
                .headers(encabezados)
                .contentType(MediaType.TEXT_PLAIN)
                .body(contenido);
    }

    /*
     * Endpoint utilizado para demostrar el balanceo.
     */
    @GetMapping(
            value = "/servidor",
            produces = MediaType.TEXT_PLAIN_VALUE
    )
    public ResponseEntity<String> identificarServidor() {

        HttpHeaders encabezados = new HttpHeaders();
        encabezados.add("X-Server-Name", serverName);

        return ResponseEntity
                .ok()
                .headers(encabezados)
                .contentType(MediaType.TEXT_PLAIN)
                .body("Respuesta generada por: " + serverName);
    }

    /*
     * Prueba sencilla para saber si la API está activa.
     */
    @GetMapping(
            value = "/estado",
            produces = MediaType.TEXT_PLAIN_VALUE
    )
    public String estado() {
        return "API funcionando correctamente en " + serverName;
    }
}