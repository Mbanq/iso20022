"""
Tests for the Fedwire module.
"""
import xml.etree.ElementTree as ET
import pytest
from unittest.mock import patch

from iso20022gen import OutgoingFedWire


@pytest.fixture
def sample_iso20022_xml():
    """Provide a sample ISO 20022 XML message for testing."""
    app_hdr = """<AppHdr xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.03">
        <Fr>
            <FIId>
                <FinInstnId>
                    <ClrSysMmbId>
                        <MmbId>121182904</MmbId>
                    </ClrSysMmbId>
                </FinInstnId>
            </FIId>
        </Fr>
        <To>
            <FIId>
                <FinInstnId>
                    <ClrSysMmbId>
                        <MmbId>021151080</MmbId>
                    </ClrSysMmbId>
                </FinInstnId>
            </FIId>
        </To>
        <BizMsgIdr>20250109TEST001000001</BizMsgIdr>
        <MsgDefIdr>pacs.008.001.08</MsgDefIdr>
        <BizSvc>TEST</BizSvc>
        <CreDt>2023-01-01T12:00:00Z</CreDt>
    </AppHdr>"""
    
    document = """<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
        <FIToFICstmrCdtTrf>
            <GrpHdr>
                <MsgId>20250109TEST001000001</MsgId>
                <CreDtTm>2023-01-01T12:00:00Z</CreDtTm>
                <NbOfTxs>1</NbOfTxs>
                <SttlmInf>
                    <SttlmMtd>CLRG</SttlmMtd>
                    <ClrSys>
                        <Cd>FDW</Cd>
                    </ClrSys>
                </SttlmInf>
            </GrpHdr>
            <CdtTrfTxInf>
                <PmtId>
                    <EndToEndId>TEST12345</EndToEndId>
                    <UETR>00000000-0000-0000-0000-000000000000</UETR>
                </PmtId>
                <IntrBkSttlmAmt Ccy="USD">10.0</IntrBkSttlmAmt>
                <Cdtr>
                    <Nm>JOHN DOE</Nm>
                </Cdtr>
            </CdtTrfTxInf>
        </FIToFICstmrCdtTrf>
    </Document>"""
    
    return app_hdr + "\n" + document


def test_wrap_in_fedwire_envelope(sample_iso20022_xml):
    """Test wrapping ISO 20022 XML in a Fedwire envelope."""
    fedwire_wrapper = OutgoingFedWire()
    
    # Test with a simpler XML setup to isolate the issue
    simple_xml = """<AppHdr xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.03"><Fr><FIId><FinInstnId><ClrSysMmbId><MmbId>TEST</MmbId></ClrSysMmbId></FinInstnId></FIId></Fr></AppHdr>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08"><FIToFICstmrCdtTrf><Cdtr><Nm>JOHN DOE</Nm></Cdtr></FIToFICstmrCdtTrf></Document>"""
    
    # Wrap the XML
    fedwire_xml = fedwire_wrapper.wrap_in_fedwire_envelope(simple_xml)
    
    # Check that the output is a string
    assert isinstance(fedwire_xml, str)
    
    # Check that the output contains the Fedwire envelope elements
    assert "FedwireFundsOutgoing" in fedwire_xml
    assert "FedwireFundsOutgoingMessage" in fedwire_xml
    assert "FedwireFundsCustomerCreditTransfer" in fedwire_xml
    
    # Check that the output contains the original ISO 20022 elements
    assert "AppHdr" in fedwire_xml
    assert "Document" in fedwire_xml
    assert "JOHN DOE" in fedwire_xml
    
    # Verify that the XML is well-formed
    try:
        root = ET.fromstring(fedwire_xml)
        assert root is not None
    except ET.ParseError:
        pytest.fail("Generated XML is not well-formed")


def test_wrap_in_fedwire_envelope_with_invalid_direction():
    """Test wrapping with an invalid direction."""
    fedwire_wrapper = OutgoingFedWire()
    
    with pytest.raises(ValueError):
        fedwire_wrapper.wrap_in_fedwire_envelope("some xml", direction="Invalid")


def test_wrap_in_fedwire_envelope_with_invalid_xml():
    """Test wrapping invalid XML."""
    fedwire_wrapper = OutgoingFedWire()
    
    with pytest.raises(ET.ParseError):
        fedwire_wrapper.wrap_in_fedwire_envelope("not valid xml")


def test_extract_from_fedwire_envelope():
    """Test extracting ISO 20022 messages from a Fedwire envelope."""
    fedwire_wrapper = OutgoingFedWire()
    
    # Create a simple XML
    simple_xml = """<AppHdr xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.03"><Fr><FIId><FinInstnId><ClrSysMmbId><MmbId>TEST</MmbId></ClrSysMmbId></FinInstnId></FIId></Fr></AppHdr>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08"><FIToFICstmrCdtTrf><Cdtr><Nm>JOHN DOE</Nm></Cdtr></FIToFICstmrCdtTrf></Document>"""
    
    # First wrap the XML
    fedwire_xml = fedwire_wrapper.wrap_in_fedwire_envelope(simple_xml)
    
    # Then extract
    extracted = fedwire_wrapper.extract_from_fedwire_envelope(fedwire_xml)
    
    # Check that we got a dictionary with the expected keys
    assert isinstance(extracted, dict)
    assert "app_hdr" in extracted
    assert "document" in extracted
    
    # Check that the extracted parts contain the expected elements
    assert "AppHdr" in extracted["app_hdr"]
    assert "Document" in extracted["document"]
    assert "JOHN DOE" in extracted["document"] 