from time import perf_counter

from app.models.schemas import QAQueryRequest, QAQueryResponse


def answer_question(payload: QAQueryRequest) -> QAQueryResponse:
    start = perf_counter()
    question = payload.question.strip()

    if payload.mode == "rag":
        answer = (
            "[RAG] 요청하신 내용을 매뉴얼 근거 기반으로 요약합니다. "
            f"질문: '{question}'.\n"
            "1) 메뉴 경로를 확인하고 2) 절차를 순서대로 수행하세요."
        )
        sources = ["manual_v1.pdf#p12", "manual_v1.pdf#p19"]
    else:
        answer = (
            "[LLM Only] 일반 지식 기반 안내입니다. "
            f"질문: '{question}'.\n"
            "환경별 차이가 있을 수 있으므로 실제 화면과 비교 확인하세요."
        )
        sources = []

    latency_ms = int((perf_counter() - start) * 1000) + 30
    tokens_in = max(20, len(question) // 2)
    tokens_out = max(50, len(answer) // 3)

    return QAQueryResponse(
        answer=answer,
        mode=payload.mode,
        sources=sources,
        latency_ms=latency_ms,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
    )
