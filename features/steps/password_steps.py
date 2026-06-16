import sys
import os
# pyrefly: ignore [missing-import]
from behave import given, when, then

# Agregar src al path para importar password_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
# pyrefly: ignore [missing-import]
import password_manager

# =============================================
# Steps originales (password.feature)
# =============================================

@given('una contraseña propuesta "{password}"')
def step_impl_given_password(context, password):
    context.proposed_password = password

@when('valido la contraseña')
def step_impl_validate(context):
    context.validation_result = password_manager.validate_password(context.proposed_password)

@then('la contraseña es rechazada')
def step_impl_rejected(context):
    assert not context.validation_result['valid'], "Se esperaba que la contraseña fuera inválida"

@then('se muestran los errores correspondientes')
def step_impl_errors(context):
    assert len(context.validation_result['errors']) > 0, "Debería haber errores de validación"

@then('la contraseña es aceptada sin errores')
def step_impl_accepted(context):
    assert context.validation_result['valid'], f"Errores: {context.validation_result['errors']}"

@given('las palabras base "{words}"')
def step_impl_base_words(context, words):
    context.base_words = words

@when('genero una contraseña basada en palabras')
def step_impl_generate_words(context):
    context.generated_password = password_manager.generate_from_words(context.base_words)

@then('la contraseña generada es validada como segura')
def step_impl_validate_generated(context):
    result = password_manager.validate_password(context.generated_password)
    assert result['valid'], f"Contraseña generada: {context.generated_password}. Errores: {result['errors']}"

@when('genero una contraseña aleatoria')
def step_impl_generate_random(context):
    context.generated_password = password_manager.generate_random()

# =============================================
# Steps para password_v2.feature
# =============================================

@given('el usuario proporciona una entrada base como "{words}"')
def step_impl_v2_input(context, words):
    context.input_words = words

@when('el usuario solicita generar las contraseñas')
def step_impl_v2_generate(context):
    context.generated_passwords = password_manager.generate_multiple_from_words(context.input_words)

@then('el sistema debe generar y mostrar simultáneamente {count:d} contraseñas:')
def step_impl_v2_count(context, count):
    assert len(context.generated_passwords) == count, \
        f"Se esperaban {count} contraseñas, se obtuvieron {len(context.generated_passwords)}"

@then('todas las contraseñas generadas deben cumplir con las 5 políticas de seguridad')
def step_impl_v2_all_valid(context):
    for i, pwd in enumerate(context.generated_passwords):
        result = password_manager.validate_password(pwd)
        assert result['valid'], \
            f"Contraseña #{i+1} ({pwd}) no cumple las políticas. Errores: {result['errors']}"

@given('que el probador de contraseñas evalúa las políticas en tiempo real')
def step_impl_v2_checker_ready(context):
    # El probador está listo — no se requiere setup adicional
    pass

@when('el usuario evalúa la contraseña "{password}" en el probador')
def step_impl_v2_evaluate(context, password):
    context.detailed_result = password_manager.validate_password_detailed(password)

@then('el sistema debe indicar el estado exacto de cada requisito:')
def step_impl_v2_check_requirements(context):
    check_map = {
        'Longitud >= 12': 'length',
        'Contiene Mayúscula': 'uppercase',
        'Contiene Minúscula': 'lowercase',
        'Contiene Número': 'number',
        'Contiene Especial': 'special',
    }
    estado_map = {
        'Verdadero': True,
        'Falso': False,
    }

    for row in context.table:
        requisito = row['Requisito']
        esperado_str = row['Estado esperado']
        check_key = check_map[requisito]
        esperado = estado_map[esperado_str]
        actual = context.detailed_result['checks'][check_key]
        assert actual == esperado, \
            f"Requisito '{requisito}': esperado={esperado}, actual={actual}"
