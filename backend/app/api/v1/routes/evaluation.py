import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, Response
from app.core.pipeline import stream_evaluation
from app.services.export_service import export_pdf, export_docx, export_xlsx
from app.utils.document_parser import parse_bytes
from app.schemas.models import EvaluationReport

router = APIRouter(prefix="/evaluate", tags=["evaluation"])


@router.post("/stream")
async def evaluate_stream(
    rfp_file: UploadFile = File(...),
    proposal_file: UploadFile = File(...),
    vendor_name: str = Form(default="Vendor"),
):
    rfp_bytes = await rfp_file.read()
    proposal_bytes = await proposal_file.read()
    rfp_text = parse_bytes(rfp_bytes, rfp_file.filename or "rfp.txt")
    proposal_text = parse_bytes(proposal_bytes, proposal_file.filename or "proposal.txt")

    if not rfp_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from RFP file")
    if not proposal_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from proposal file")

    async def event_generator():
        async for event in stream_evaluation(rfp_text, proposal_text, vendor_name):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/text")
async def evaluate_text(
    rfp_text: str = Form(...),
    proposal_text: str = Form(...),
    vendor_name: str = Form(default="Vendor"),
):
    async def event_generator():
        async for event in stream_evaluation(rfp_text, proposal_text, vendor_name):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/export/pdf")
async def export_report_pdf(report: EvaluationReport):
    pdf_bytes = export_pdf(report)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="rfp_report_{report.vendor_name.replace(" ","_")}.pdf"'},
    )


@router.post("/export/docx")
async def export_report_docx(report: EvaluationReport):
    docx_bytes = export_docx(report)
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="rfp_report_{report.vendor_name.replace(" ","_")}.docx"'},
    )


@router.post("/export/xlsx")
async def export_report_xlsx(report: EvaluationReport):
    xlsx_bytes = export_xlsx(report)
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="rfp_report_{report.vendor_name.replace(" ","_")}.xlsx"'},
    )
