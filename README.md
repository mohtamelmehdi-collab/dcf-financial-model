# 📊 Excel VBA — Accounting Automation

> Automated accounting tools built in Excel VBA for bank reconciliation and fixed asset management.  
> Developed as part of my professional accounting practice.

---

## 🔒 Security Notice

All data used in this repository is **100% fictitious**.  
No real company data, supplier names, or bank account numbers are included.  
Do not publish sensitive or confidential data in any fork of this project.

---

## 📁 Project Structure

```
vba-accounting-automation/
│
├── BankReconciliation.bas    # Automated bank-to-GL reconciliation
├── FixedAssets.bas           # Fixed asset register & depreciation calculator
├── sample_data/
│   ├── BankStatement_FICTITIOUS.xlsx   # Sample bank statement (fake data)
│   └── GeneralLedger_FICTITIOUS.xlsx   # Sample GL extract (fake data)
└── README.md
```

---

## ⚙️ Features

### 🏦 Bank Reconciliation (`BankReconciliation.bas`)
- Imports bank statement entries and GL entries
- Matches transactions by **amount** (tolerance ±0.01 MAD)
- Generates a color-coded reconciliation report:
  - ✔ **Green** = Matched
  - ✘ **Red** = Unmatched
- Calculates reconciliation rate automatically
- Navy/Gold formatting for professional output

### 🏗️ Fixed Assets (`FixedAssets.bas`)
- Manages 100+ industrial assets
- Calculates **linear depreciation** per asset
- Computes:
  - Annual depreciation (Dotation annuelle)
  - Accumulated depreciation (Amortissements cumulés)
  - Net book value (Valeur Nette Comptable)
- Color flags: 🔴 Fully depreciated / 🟡 Near end of life
- Generates summary report with totals

---

## 🚀 How to Use

1. Open Excel and press `Alt + F11` to open the VBA editor
2. Import the `.bas` modules: `File > Import File`
3. Create sheets named:
   - `Relevé_Banque` (bank statement)
   - `Grand_Livre` (general ledger)
   - `Réconciliation` (results output)
   - `Immobilisations` (asset register)
   - `Dotations` (depreciation output)
4. Run macros from `Alt + F8`

---

## 📐 Sheet Structure Expected

### Relevé_Banque / Grand_Livre
| Column | Content |
|--------|---------|
| A | Date |
| B | Reference |
| C | Label / Description |
| D | Amount (MAD) |
| E | Status (for GL matching) |

### Immobilisations
| Column | Content |
|--------|---------|
| A | Asset Code |
| B | Asset Name |
| C | Acquisition Date |
| D | Cost Value (MAD) |
| E | Useful Life (years) |

---

## 🛠️ Technologies

- Microsoft Excel (2016+)
- VBA (Visual Basic for Applications)
- Moroccan accounting standards (CGNC / CGI)

---

## 👨‍💼 Author

**El Mahdi Mohtam**  
Cost & Asset Accountant | Financial Modeling Enthusiast  
📍 Morocco | 🌐 [Portfolio](https://mohtamprofil.netlify.app)  
🔗 [LinkedIn](https://linkedin.com/in/m-elmahdi-mohtam)

---

## 📄 License

MIT License — Free to use and adapt with attribution.
