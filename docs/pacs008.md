# PACS.008 Message Documentation

## Overview

The PACS.008 (FIToFICstmrCdtTrf - FinancialInstitutionToFinancialInstitutionCustomerCreditTransfer) message is used to move funds from a debtor to a creditor through financial institutions. It is commonly used in the context of customer credit transfers between financial institutions.

## Message Components

### 1. Document

```xml
<pacs:Document xmlns:pacs="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
    <pacs:FIToFICstmrCdtTrf>
        <pacs:GrpHdr>
            <pacs:MsgId>20250109MBANQ001000001</pacs:MsgId>
            <pacs:CreDtTm>2025-04-28T23:02:43.980623+00:00</pacs:CreDtTm>
            <pacs:NbOfTxs>1</pacs:NbOfTxs>
            <pacs:SttlmInf>
                <pacs:SttlmMtd>CLRG</pacs:SttlmMtd>
                <pacs:ClrSys>
                    <pacs:Cd>FDW</pacs:Cd>
                </pacs:ClrSys>
            </pacs:SttlmInf>
        </pacs:GrpHdr>
        <!-- Credit Transfer Information -->
    </pacs:FIToFICstmrCdtTrf>
</pacs:Document>
```

#### 2.1 Group Header (`GrpHdr`)
- `MsgId`: Same as BizMsgIdr from header
- `CreDtTm`: Creation timestamp
- `NbOfTxs`: Number of transactions (typically 1)
- `SttlmInf`: 
  - `SttlmMtd`: "CLRG" for clearing
  - `ClrSys/Cd`: "FDW" for Fedwire

#### 2.2 Credit Transfer Information (`CdtTrfTxInf`)

```xml
<pacs:CdtTrfTxInf>
    <pacs:PmtId>
        <pacs:EndToEndId>MEtoEID3SrEEU7G</pacs:EndToEndId>
        <pacs:UETR>6aacb6b3-1e69-49d6-9ea6-157d62fceb94</pacs:UETR>
    </pacs:PmtId>
    <pacs:IntrBkSttlmAmt Ccy="USD">10.0</pacs:IntrBkSttlmAmt>
    <pacs:IntrBkSttlmDt>2025-01-09</pacs:IntrBkSttlmDt>
    <pacs:ChrgBr>SLEV</pacs:ChrgBr>
</pacs:CdtTrfTxInf>
```

Key components:
1. Payment Identification:
   - `EndToEndId`: Unique identifier (format: MEtoEID + random string)
   - `UETR`: Universal unique identifier (UUID)

2. Payment Type:
   ```xml
   <pacs:PmtTpInf>
       <pacs:LclInstrm>
           <pacs:Prtry>CTRC</pacs:Prtry>
       </pacs:LclInstrm>
   </pacs:PmtTpInf>
   ```

3. Amount Information:
   - `IntrBkSttlmAmt`: Settlement amount with currency
   - `InstdAmt`: Instructed amount (usually same as settlement)
   - `IntrBkSttlmDt`: Settlement date

4. Financial Institution Information:
   ```xml
   <pacs:InstgAgt>
       <pacs:FinInstnId>
           <pacs:ClrSysMmbId>
               <pacs:ClrSysId>
                   <pacs:Cd>USABA</pacs:Cd>
               </pacs:ClrSysId>
               <pacs:MmbId>121182904</pacs:MmbId>
           </pacs:ClrSysMmbId>
       </pacs:FinInstnId>
   </pacs:InstgAgt>
   ```

5. Party Information:
   ```xml
   <pacs:Dbtr>
       <pacs:Nm>JANE SMITH</pacs:Nm>
       <pacs:PstlAdr>
           <pacs:AdrLine>456 OAK AVENUE</pacs:AdrLine>
           <pacs:AdrLine>SOMEWHERE, CA 67890</pacs:AdrLine>
       </pacs:PstlAdr>
   </pacs:Dbtr>
   ```

   Account information:
   ```xml
   <pacs:DbtrAcct>
       <pacs:Id>
           <pacs:Othr>
               <pacs:Id>550103129900943</pacs:Id>
           </pacs:Othr>
       </pacs:Id>
   </pacs:DbtrAcct>
   ```

## Field Specifications

1. **Identifiers**:
   - ABA routing numbers: 9-digit format
   - Account numbers: Variable length
   - EndToEndId: "MEtoEID" prefix + random string
   - UETR: Standard UUID format

2. **Amounts**:
   - Currency: 3-letter ISO code (e.g., "USD")
   - Value: Decimal number with point separator

3. **Dates**:
   - Format: ISO 8601 (YYYY-MM-DD)
   - Timestamps: ISO 8601 with timezone (YYYY-MM-DDThh:mm:ss.nnnnnnn+hh:mm)

4. **Addresses**:
   - Two lines format
   - Line 1: Street address
   - Line 2: City, State ZIP

## Required Fields

1. Message Header:
   - Fr/To with valid ABA numbers
   - BizMsgIdr
   - MsgDefIdr
   - CreDt

2. Document:
   - GrpHdr with MsgId and settlement info
   - CdtTrfTxInf with:
     - Payment identification
     - Amount information
     - Settlement date
     - Debtor/Creditor information
     - Account information
