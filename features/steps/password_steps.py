import sys
import os
# pyrefly: ignore [missing-import]
from behave import given, when, then

# Agregar src al path para importar password_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
# pyrefly: ignore [missing-import]
import password_manager

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
