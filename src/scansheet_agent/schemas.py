from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, field_validator


class DocumentTypeEnum(Enum):
    """Enum for document types"""

    FICHA_CADASTRO_INDIVIDUAL = "ficha_cadastro_individual"
    OUTROS = "outros"


class FichaCadastroIndividualContent(BaseModel):
    """Model for Ficha de Cadastro Individual content"""
    digitado_por: Optional[str] = None
    conferido_por: Optional[str] = None
    num_folha: Optional[str] = None
    dt_preenchimento: Optional[date] = None
    cns_prof: Optional[str] = None
    cbo: Optional[str] = None
    cnes: Optional[str] = None
    ine: Optional[str] = None
    dt_ficha: Optional[date] = None
    cns_cpf_cidadao: Optional[str] = None
    fl_cidadao_respon_familiar: Optional[bool] = None
    cns_cpf_respon_familiar: Optional[str] = None
    microarea: Optional[str] = None
    nm_completo: Optional[str] = None
    nm_social: Optional[str] = None
    dt_nasc: Optional[date] = None
    sexo: Optional[str] = None
    raca_cor: Optional[str] = None
    etnia: Optional[str] = None
    nis: Optional[str] = None
    nm_completo_mae: Optional[str] = None
    nm_completo_pai: Optional[str] = None
    nacionalidade: Optional[str] = None
    pais_nasc: Optional[str] = None
    dt_naturalizacao: Optional[date] = None
    portaria_naturaliz: Optional[str] = None
    municipio_uf_nasc: Optional[str] = None
    dt_entrada_brasil: Optional[date] = None
    tel_cel: Optional[str] = None
    email: Optional[str] = None
    ocupacao: Optional[str] = None
    situac_mercado_trab: Optional[str] = None
    rel_parentesco_responsavel_familiar: Optional[str] = None
    fl_freq_escola_ou_creche: Optional[bool] = None
    curso_mais_elevado: Optional[str] = None
    ls_criancas_0_a_9_anos_quem_fica: Optional[List[str]] = []
    fl_freq_cuidador_trad: Optional[bool] = None
    fl_part_gp_comunitario: Optional[bool] = None
    fl_possui_plano_saude_priv: Optional[bool] = None
    fl_membro_povo_comunidade_trad: Optional[bool] = None
    nm_povo_comunidade_trad: Optional[str] = None
    fl_informar_orientacao_sexual: Optional[bool] = None
    orientacao_sexual: Optional[str] = None
    fl_informar_identidade_genero: Optional[bool] = None
    identidade_genero: Optional[str] = None
    fl_deficiencia: Optional[bool] = None
    ls_deficiencia: Optional[List[str]] = []
    fl_tria_1: Optional[bool] = None
    fl_tria_2: Optional[bool] = None
    fl_saida_cadast: Optional[bool] = None
    dt_obito: Optional[date] = None
    num_do: Optional[str] = None
    fl_gestante: Optional[bool] = None
    maternidade_referencia: Optional[str] = None
    peso_considera: Optional[str] = None
    fl_doenc_resp_pulmao: Optional[bool] = None
    ls_doenc_resp_pulmao: Optional[List[str]] = []
    fl_fumante: Optional[bool] = None
    fl_alcool: Optional[bool] = None
    fl_outras_drogas: Optional[bool] = None
    fl_hanseniase: Optional[bool] = None
    fl_tuberculose: Optional[bool] = None
    fl_hipertensao_arterial: Optional[bool] = None
    fl_tem_ou_teve_cancer: Optional[bool] = None
    fl_diabetes: Optional[bool] = None
    fl_internacao_ultimos_12_meses: Optional[bool] = None
    causa_internacao_ultimos_12_meses: Optional[str] = None
    fl_avc_derrame: Optional[bool] = None
    fl_infarto: Optional[bool] = None
    fl_saude_mental: Optional[bool] = None
    fl_doenc_cardiaca: Optional[bool] = None
    ls_doenc_cardiaca: Optional[List[str]] = []
    fl_acamado: Optional[bool] = None
    fl_domiciliado: Optional[bool] = None
    fl_plantas_medicinais: Optional[bool] = None
    plantas_medicinais: Optional[str] = None
    fl_problemas_rins: Optional[bool] = None
    ls_problemas_rins: Optional[List[str]] = []
    fl_outras_praticas: Optional[bool] = None
    outras_condicoes_saude_1: Optional[bool] = None
    outras_condicoes_saude_2: Optional[bool] = None
    outras_condicoes_saude_3: Optional[bool] = None
    fl_situacao_rua: Optional[bool] = None
    tempo_situacao_rua: Optional[str] = None
    fl_acompanhado_outra_institu: Optional[bool] = None
    instituicao_acompanhamento: Optional[str] = None
    fl_beneficio: Optional[bool] = None
    fl_referencia_familiar: Optional[bool] = None
    fl_visita_familiar: Optional[bool] = None
    grau_parentesco_visita: Optional[str] = None
    fl_higiene_pessoal: Optional[bool] = None
    ls_higiene_pessoal: Optional[List[str]] = []
    alimentacao_diaria: Optional[str] = None
    ls_origem_alimentacao: Optional[List[str]] = []

    @field_validator('dt_ficha', 'dt_nasc', 'dt_naturalizacao', 'dt_entrada_brasil', 'dt_obito')
    def validate_date_format(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%m-%d-%Y").date()
            except ValueError:
                raise ValueError('Date must be in MM-DD-YYYY format')
        return v

    @field_validator('*')
    def validate_fl_fields(cls, v, info):
        if info.field_name.startswith('fl_') and v is not None:
            if isinstance(v, bool):
                return v
            else:
                raise ValueError(f'Field {info.field_name} must be a boolean')
        return v

    @field_validator('*')
    def validate_ls_fields(cls, v, info):
        if info.field_name.startswith('ls_') and v is not None:
            if isinstance(v, list):
                return v
            else:
                raise ValueError(f'Field {info.field_name} must be a list')
        return v


class AIMessageModel(BaseModel):
    """"Agent Message Model"""

    title: DocumentTypeEnum
    content: FichaCadastroIndividualContent | dict

    @field_validator('content')
    def validate_content_for_title(cls, v, values):
        if 'title' in values and values['title'] == DocumentTypeEnum.OUTROS:
            if not isinstance(v, dict):
                raise ValueError('Content must be a dictionary for title "OUTROS"')

        if 'title' in values and values['title'] == DocumentTypeEnum.FICHA_CADASTRO_INDIVIDUAL:
            if not isinstance(v, FichaCadastroIndividualContent):
                raise ValueError(
                    'Content must be of type FichaCadastroIndividualContent for title "FICHA_CADASTRO_INDIVIDUAL"')
        return v
