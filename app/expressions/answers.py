from sqlalchemy import func, select, case, literal_column, text
from sqlalchemy.orm import aliased
from app.entities.answers import Answer
from app.entities.surveys import Survey


def get_upload_files_quantity_expression():
    """
    Подсчитывает количество загруженных файлов в ответе
    Использует простой подход с jsonb_array_length
    """
    return func.coalesce(
        func.jsonb_array_length(
            func.jsonb_array_elements(
                func.jsonb_object_values(Answer.uploads)
            )
        ),
        0
    ).label('upload_files_quantity')


def get_total_files_quantity_expression():
    """
    Подсчитывает общее количество полей для загрузки файлов в опросе
    Использует простой подход с jsonb_array_length
    """
    return func.coalesce(
        func.jsonb_array_length(
            func.jsonb_array_elements(
                func.jsonb_extract_path(
                    func.jsonb_array_elements(
                        func.jsonb_extract_path(Survey.data, 'sections')
                    ),
                    'uploads'
                )
            )
        ),
        0
    ).label('total_files_quantity')


def get_answers_with_file_counts():
    """
    Возвращает CTE с подсчитанными количествами файлов для каждого ответа
    """
    from sqlalchemy import text
    
    # CTE для подсчета файлов
    file_counts_cte = select(
        Answer.id,
        get_upload_files_quantity_expression(),
        get_total_files_quantity_expression()
    ).cte('file_counts')
    
    return file_counts_cte


def get_answers_with_file_stats():
    """
    Возвращает подзапрос с полной статистикой по файлам
    """
    return select(
        Answer.id,
        Answer.survey_id,
        Answer.data,
        Answer.uploads,
        Answer.status,
        Answer.submitted_at,
        Answer.created_at,
        Answer.updated_at,
        get_upload_files_quantity_expression(),
        get_total_files_quantity_expression(),
        # Дополнительная статистика
        case(
            (get_total_files_quantity_expression() > 0, 
             func.round(
                 get_upload_files_quantity_expression() * 100.0 / get_total_files_quantity_expression(), 
                 2
             )),
            else_=0
        ).label('upload_percentage'),
        # Статус загрузки файлов
        case(
            (get_upload_files_quantity_expression() == 0, 'no_files'),
            (get_upload_files_quantity_expression() < get_total_files_quantity_expression(), 'partial'),
            else_='complete'
        ).label('file_upload_status')
    ).select_from(
        Answer.__table__.join(Survey.__table__, Answer.survey_id == Survey.id)
    )
