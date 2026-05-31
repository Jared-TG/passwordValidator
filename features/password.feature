Feature: Generación y Validación de Contraseñas Seguras
  Para asegurar la protección de mis cuentas
  Como usuario del sistema
  Quiero generar contraseñas seguras y validar que cumplen con las políticas

  Scenario: Validar una contraseña débil
    Given una contraseña propuesta "Hola123"
    When valido la contraseña
    Then la contraseña es rechazada
    And se muestran los errores correspondientes

  Scenario: Validar una contraseña que cumple las políticas
    Given una contraseña propuesta "SuperSegura123!"
    When valido la contraseña
    Then la contraseña es aceptada sin errores

  Scenario: Generar contraseña a partir de palabras
    Given las palabras base "mi perro salta"
    When genero una contraseña basada en palabras
    Then la contraseña generada es validada como segura

  Scenario: Generar contraseña aleatoria
    When genero una contraseña aleatoria
    Then la contraseña generada es validada como segura
