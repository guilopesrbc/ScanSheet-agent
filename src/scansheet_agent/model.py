from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, field_validator


class DocumentTypeEnum(Enum):
    """Enum for document types"""

    FICHA_CADASTRO_INDIVIDUAL = "ficha_cadastro_individual"


class FichaCadastroIndividualContent(BaseModel):
    digitado_por: Optional[str] = None
    conferido_por: Optional[str] = None
    num_folha: Optional[str] = None
    cns_prof: Optional[str] = None,
    cbo: Optional[str] = None,
    cnes: Optional[str] = None,
    ine: Optional[str] = None,
    dt_ficha: Optional[date] = None
    cns_cpf_cidadao: Optional[str] = None
    fl_cidadao_respon_familiar: Optional[str] = None
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
    fl_freq_escola_ou_creche: Optional[str] = None
    curso_mais_elevado: Optional[str] = None
    criancas_0_a_9_anos_quem_fica: Optional[List[str]] = []
    fl_freq_cuidador_trad: Optional[str] = None
    fl_part_gp_comunitario: Optional[str] = None
    fl_possui_plano_saude_priv: Optional[str] = None
    fl_membro_povo_comunidade_trad: Optional[str] = None
    nm_povo_comunidade_trad: Optional[str] = None
    fl_informar_orientacao_sexual: Optional[str] = None
    orientacao_sexual: Optional[str] = None
    fl_informar_identidade_genero: Optional[str] = None
    identidade_genero: Optional[str] = None
    fl_deficiencia: Optional[str] = None
    deficiencia: Optional[List[str]] = []
    fl_tria_1: Optional[str] = None
    fl_tria_2: Optional[str] = None
    fl_saida_cadast: Optional[str] = None
    dt_obito: Optional[date] = None
    num_do: Optional[str] = None
    fl_gestante: Optional[str] = None
    maternidade_referencia: Optional[str] = None
    peso_considera: Optional[str] = None
    fl_doenc_resp_pulmao: Optional[str] = None
    doenc_resp_pulmao: Optional[List[str]] = []
    fl_fumante: Optional[str] = None
    fl_alcool: Optional[str] = None
    fl_outras_drogas: Optional[str] = None
    fl_hanseniase: Optional[str] = None
    fl_tuberculose: Optional[str] = None
    fl_hipertensao_arterial: Optional[str] = None
    fl_tem_ou_teve_cancer: Optional[str] = None
    fl_diabetes: Optional[str] = None
    fl_internacao_ultimos_12_meses: Optional[str] = None
    causa_internacao_ultimos_12_meses: Optional[str] = None
    fl_avc_derrame: Optional[str] = None
    fl_infarto: Optional[str] = None
    fl_problema_saude_mental: Optional[str] = None
    fl_doenc_cardi_coracao: Optional[str] = None
    doenc_cardi_coracao: Optional[List[str]] = []
    fl_acamado: Optional[str] = None
    fl_domiciliado: Optional[str] = None
    fl_plantas_medicinais: Optional[str] = None
    plantas_medicinais: Optional[str] = None
    fl_problemas_nos_rins: Optional[str] = None
    problemas_nos_rins: Optional[List[str]] = []
    fl_prat_integrativas_e_compl: Optional[str] = None
    outras_condicoes_saude: Optional[List[str]] = []
    fl_situacao_rua: Optional[str] = None
    tempo_em_situacao_rua: Optional[str] = None
    fl_acompanhado_outra_institu: Optional[str] = None
    instituicao: Optional[str] = None
    fl_beneficio: Optional[str] = None
    fl_possui_ref_fami: Optional[str] = None
    fl_visita_fami: Optional[str] = None
    grau_parentesco: Optional[str] = None
    fl_higiene_pessoal: Optional[str] = None
    higiene_pessoal: Optional[List[str]] = []
    alimentacao_ao_dia: Optional[str] = None
    origem_alimentacao: Optional[List[str]] = []

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
            normalized = v.lower().strip()
            normalized = normalized.replace('não', 'nao')
            if normalized not in ['sim', 'nao']:
                raise ValueError(f'Field {info.field_name} must be "sim" or "nao"')
            return normalized
        return v


class AIMessageModel(BaseModel):
    """"Agent Message Model"""

    title: DocumentTypeEnum
    content: FichaCadastroIndividualContent

