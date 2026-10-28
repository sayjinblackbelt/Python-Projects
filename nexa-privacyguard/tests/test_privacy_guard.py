
import pytest

from privacy_guard import is_valid_cpf, mask_text, scan_text


def test_detect_email():
    findings = scan_text("Contato: exemplo@teste.com")
    assert any(item.category == "EMAIL" for item in findings)


def test_detect_valid_cpf():
    findings = scan_text("CPF: 529.982.247-25")
    assert any(item.category == "CPF" for item in findings)


def test_detect_invalid_cpf_as_suspicious():
    findings = scan_text("CPF: 123.456.789-00")
    assert any(item.category == "CPF_SUSPEITO" for item in findings)


def test_repeated_digit_cpf_is_invalid():
    assert is_valid_cpf("111.111.111-11") is False


def test_detect_brazilian_phone():
    findings = scan_text("Telefone: (19) 98765-4321")
    assert any(item.category == "TELEFONE" for item in findings)


def test_detect_token_value():
    findings = scan_text("api_key=abcDEF123456xyz")
    token = next(item for item in findings if item.category == "TOKEN")
    assert token.value == "abcDEF123456xyz"


def test_mask_multiple_categories():
    original = (
        "E-mail: exemplo@teste.com; "
        "CPF: 529.982.247-25; "
        "Telefone: (19) 98765-4321"
    )

    masked = mask_text(original)

    assert "[EMAIL]" in masked
    assert "[CPF]" in masked
    assert "[TELEFONE]" in masked
    assert "exemplo@teste.com" not in masked
    assert "529.982.247-25" not in masked
    assert "(19) 98765-4321" not in masked


def test_mask_suspicious_cpf():
    masked = mask_text("CPF: 123.456.789-00")
    assert masked == "CPF: [CPF_SUSPEITO]"


def test_mask_token_value_but_keep_field_name():
    masked = mask_text("api_key=abcDEF123456xyz")
    assert masked == "api_key=[TOKEN]"
    assert "abcDEF123456xyz" not in masked


def test_text_without_findings_is_unchanged():
    original = "Este texto contém apenas informações comuns."
    assert mask_text(original) == original


def test_non_string_input_is_rejected():
    with pytest.raises(TypeError):
        scan_text(None)


def test_cpf_classification_does_not_leak_between_matches():
    text = (
        "CPF válido: 529.982.247-25; "
        "CPF suspeito: 123.456.789-00; "
        "Outro CPF válido: 529.982.247-25"
    )

    cpf_findings = [
        item for item in scan_text(text)
        if item.category.startswith("CPF")
    ]

    assert [item.category for item in cpf_findings] == [
        "CPF",
        "CPF_SUSPEITO",
        "CPF",
    ]
