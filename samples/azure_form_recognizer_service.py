import asyncio
from pathlib import Path

from azure_python.common.form_recognizer_parse import parse
from azure_python.hosting import container
from azure_python.protocols.i_azure_form_recognizer import IAzureFormRecognizer

current_path = Path(__file__).parent.parent
sample = current_path / "test_data" / "ast_sci_data_tables_sample.pdf"


async def main() -> None:
    svc = container[IAzureFormRecognizer]
    result = await svc.analyze_document(sample)
    if result:
        print("\n".join(parse(result)))


if __name__ == "__main__":
    asyncio.run(main())
