Feature: Generación Múltiple de Contraseñas y Probador Interactivo
  Para ofrecer opciones versátiles y enseñar sobre seguridad
  Como usuario del sistema
  Quiero generar 4 tipos distintos de contraseñas desde una sola entrada y tener un probador visual de requisitos

  Scenario: Generación de 4 tipos de contraseña a partir de una única entrada
    Given el usuario proporciona una entrada base como "mi perro"
    When el usuario solicita generar las contraseñas
    Then el sistema debe generar y mostrar simultáneamente 4 contraseñas:
      | Tipo                  | Descripción                                               |
      | Basada en palabras    | Mantiene la base concatenada y rellena lo faltante        |
      | Memorable (Leet speak)| Aplica sustituciones (ej. a->@, e->3) para legibilidad    |
      | CamelCase + Símbolos  | Capitaliza palabras e intercala números y símbolos        |
      | Aleatoria             | Genera 16 caracteres de forma completamente aleatoria     |
    And todas las contraseñas generadas deben cumplir con las 5 políticas de seguridad

  Scenario Outline: Probador de contraseñas mostrando requerimientos individuales
    Given que el probador de contraseñas evalúa las políticas en tiempo real
    When el usuario evalúa la contraseña "<password>" en el probador
    Then el sistema debe indicar el estado exacto de cada requisito:
      | Requisito           | Estado esperado   |
      | Longitud >= 12      | <check_longitud>  |
      | Contiene Mayúscula  | <check_mayus>     |
      | Contiene Minúscula  | <check_minus>     |
      | Contiene Número     | <check_num>       |
      | Contiene Especial   | <check_especial>  |

    Examples:
      | password       | check_longitud | check_mayus | check_minus | check_num | check_especial |
      | gatito12       | Falso          | Falso       | Verdadero   | Verdadero | Falso          |
      | GATITO123!!!   | Verdadero      | Verdadero   | Falso       | Verdadero | Verdadero      |
      | P@ssw0rd123456 | Verdadero      | Verdadero   | Verdadero   | Verdadero | Verdadero      |
