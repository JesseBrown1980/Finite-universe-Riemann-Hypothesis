#!/usr/bin/env python3
"""Generate publication-quality PDF report for Host8 Riemann Hypothesis Phase 5."""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        footer_text = f"Host8 Ternary Riemann Hypothesis Analogue — Phase 5 Verification Report | Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 0.5 * inch, 0.4 * inch, footer_text)
        self.drawString(0.5 * inch, 0.4 * inch, "CONFIDENTIAL / RESEARCH ARCHIVE — EXACT ARITHMETIC")
        self.setStrokeColor(colors.HexColor("#cccccc"))
        self.setLineWidth(0.5)
        self.line(0.5 * inch, 0.55 * inch, letter[0] - 0.5 * inch, 0.55 * inch)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f2b48'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2c5282'),
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f2b48'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#222222'),
        spaceAfter=6
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#9c4221')
    )
    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#222222')
    )
    cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0f2b48')
    )
    cell_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("Host8 Ternary Finite-Field Riemann Hypothesis Analogue", title_style))
    elements.append(Paragraph("Phase 5 Audit: 375-Sector Physical Volume Sweep, Formal Frobenius Lift Modulo 9, and Discrete Substrate Dynamics", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0f2b48'), spaceAfter=10))

    # Executive Summary
    elements.append(Paragraph("1. Executive Summary & Verification Status", h1_style))
    exec_summary_text = (
        "This report consolidates the complete experimental, physical, and algebraic audit of the Host8 "
        "finite-universe Riemann Hypothesis analogue across GitHub commit <b>eded2e4</b> on "
        "<b>JesseBrown1980/Finite-universe-Riemann-Hypothesis</b>. The execution spans five synchronized phases: "
        "(1) exact Weil RH point-enumeration over ternary extension fields, (2) controlled 27-mode circulant spectral analysis, "
        "(3) four-dimensional Frobenius companion holdouts, (4) direct differential Cartier–Manin / Hasse–Witt invariants, "
        "and (5) a fail-closed 375-sector distributed sampling sweep across the physical 300 GB volume alongside a formal "
        "Frobenius lift modulo 9. All computations use exact integer arithmetic with zero floating-point root tolerances."
    )
    elements.append(Paragraph(exec_summary_text, body_style))

    # Master Table
    t1_data = [
        [Paragraph("Verification Layer", cell_header), Paragraph("Physical Scope / Dataset", cell_header), Paragraph("Observed Invariant", cell_header), Paragraph("Status", cell_header)],
        [Paragraph("<b>Published Slice Hashes</b>", cell_style), Paragraph("Sectors 000, 187, 374 (2.53 MiB)", cell_style), Paragraph("6 / 6 exact SHA-256 match", cell_style), Paragraph("<b>100% PASS</b>", cell_bold)],
        [Paragraph("<b>Phase 1: Weil RH Analogue</b>", cell_style), Paragraph("288 Host8 rooms + 243 quintics", cell_style), Paragraph("194 Host8 & 162 exhaustive curves pass RH", cell_style), Paragraph("<b>100% PASS</b>", cell_bold)],
        [Paragraph("<b>Phase 2: 27-Mode Spectrum</b>", cell_style), Paragraph("27x27 circulant H over F_1000081", cell_style), Paragraph("Lambda + Lambda' = 1 mod P; X[0] = 0 mod P", cell_style), Paragraph("<b>100% PASS</b>", cell_bold)],
        [Paragraph("<b>Phase 3: Frobenius Companion</b>", cell_style), Paragraph("388 Host8 + 324 exhaustive holdouts", cell_style), Paragraph("Exact point prediction over F_243 & F_729", cell_style), Paragraph("<b>100% PASS</b>", cell_bold)],
        [Paragraph("<b>Phase 4: Cartier-Manin Operator</b>", cell_style), Paragraph("162 curves via H^0(C, Omega^1)", cell_style), Paragraph("Tr(C) = -A mod 3, det(C) = B mod 3", cell_style), Paragraph("<b>100% PASS</b>", cell_bold)],
        [Paragraph("<b>Phase 5A: 375-Sector Sweep</b>", cell_style), Paragraph("375 sectors, 72,000 rooms on D:", cell_style), Paragraph("48,252 smooth genus-2 curves pass RH", cell_style), Paragraph("<b>100% PASS</b>", cell_bold)],
        [Paragraph("<b>Phase 5B: Formal Lift Mod 9</b>", cell_style), Paragraph("162 exhaustive + 194 Host8 curves", cell_style), Paragraph("Phi(y)^2 = f(x^3) mod 9 exact algebraic lift", cell_style), Paragraph("<b>100% PASS</b>", cell_bold)],
    ]
    t1 = Table(t1_data, colWidths=[1.8*inch, 2.3*inch, 2.3*inch, 1.1*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f2b48')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 10))

    # Epistemic Boundaries Section
    elements.append(Paragraph("2. Epistemic Demarcation & Overstatements to Avoid", h1_style))
    boundaries = [
        ("1. 'Full 300 GB Scan':",
         "The distributed 375-sector procedure checks that all 375 sector files exist and are exactly 800 MB each (300 GB total capacity), "
         "samples 72,000 physical room payloads across two grids, and verifies the 6 pinned slice SHA-256 hashes. It does <b>NOT</b> "
         "sequentially read or hash all 300 GB of raw byte streams unless explicitly executed with --hash-entire-volume (~13.5 min streaming read)."),
        ("2. Classical Riemann Hypothesis:",
         "This work verifies the finite-field analogue (Weil's theorem, 1948) for smooth projective curves over finite fields. "
         "It does <b>NOT</b> prove the classical Millennium Prize conjecture for zeta(s) on C. No mathematical bridge currently connects "
         "finite-field Frobenius eigenvalues to the critical line Re(s) = 1/2 of classical zeta(s)."),
        ("3. Published Slices vs. Physical Drive:",
         "The six reference SHA-256 hashes authenticate approximately <b>2.53 MiB</b> of committed binary slices from commit 5a7e9a2. "
         "They do not form a cryptographic root Merkle hash for the remaining uncommitted bytes of the 300 GB volume."),
        ("4. Skew-Circulant Symmetries vs. Prime Ladder:",
         "The reflection lambda + lambda' = 1 mod P and the uncomputed center invariant X[0] = 0 mod P are universal structural consequences "
         "of skew-circulant operators. Only even trace moments (Tr(T^2)=885145, Tr(T^4)=987346) isolate the specific prime ladder P_27[1..13]."),
        ("5. Jacobian p-Rank vs. Matrix Rank:",
         "The true geometric p-rank of Jac(C)[3] is the stable Frobenius rank f_C = rank_F3(C_HW^2), yielding 133 ordinary (p=2), "
         "35 rank-1, and 26 supersingular (p=0) curves among the 194 Host8 selections. Reporting the naive algebraic rank of C_HW is false "
         "because nilpotent rank-1 matrices have p-rank 0."),
        ("6. Hyperelliptic Bound vs. General Weil Bound:",
         "For general genus-2 curves over F_3, Weil gives |A| <= 4*sqrt(3) approx 6.928. For the monic odd-degree hyperelliptic family y^2 = f(x), "
         "evaluating over the 3 affine points of F_3 yields the strict bound A in {-3, -2, -1, 0, 1, 2, 3}. Therefore, A mod 9 uniquely and "
         "unconditionally fixes the exact integer A in Z without wrap-around.")
    ]
    for b_title, b_desc in boundaries:
        p_text = f"<b>{b_title}</b> {b_desc}"
        elements.append(Paragraph(p_text, body_style))

    elements.append(Spacer(1, 8))

    # Page Break for Physical Volume Sweep & Dynamics
    elements.append(PageBreak())

    # Section 3: Physical Volume Audit
    elements.append(Paragraph("3. Physical Host8 300 GB Volume Audit (D:\\ASOLARIA-HOST8-ROOMS-300G)", h1_style))
    elements.append(Paragraph(
        "A live physical sweep was executed using <code>scan_host8_375_sectors.py</code> against all 375 sectors "
        "on the local Windows volume. The scanner simultaneously evaluates two distinct 96-sample grids per sector: "
        "(1) Canonical Prefix Grid (rooms 0..110,591) and (2) Deep Full-Sector Grid (rooms 0..99,999,999).",
        body_style
    ))

    t2_data = [
        [Paragraph("Metric", cell_header), Paragraph("Canonical Slice Grid", cell_header), Paragraph("Deep Full-Sector Grid", cell_header), Paragraph("Combined 300 GB Totals", cell_header)],
        [Paragraph("<b>Physical Sectors Scanned</b>", cell_style), Paragraph("375 / 375", cell_style), Paragraph("375 / 375", cell_style), Paragraph("<b>375 / 375 (100.0%)</b>", cell_bold)],
        [Paragraph("<b>Physical Capacity Verified</b>", cell_style), Paragraph("800 MB / sector", cell_style), Paragraph("800 MB / sector", cell_style), Paragraph("<b>300,000,000,000 Bytes</b>", cell_bold)],
        [Paragraph("<b>Physical Room Reads</b>", cell_style), Paragraph("36,000 rooms", cell_style), Paragraph("36,000 rooms", cell_style), Paragraph("<b>72,000 rooms</b>", cell_bold)],
        [Paragraph("<b>Unique Sampled Offsets</b>", cell_style), Paragraph("35,625 positions", cell_style), Paragraph("36,000 positions", cell_style), Paragraph("<b>71,625 unique offsets</b>", cell_bold)],
        [Paragraph("<b>Smooth Genus-2 Curves</b>", cell_style), Paragraph("24,077 (66.88%)", cell_style), Paragraph("24,175 (67.15%)", cell_style), Paragraph("<b>48,252 (67.02%)</b>", cell_bold)],
        [Paragraph("<b>Finite-Field RH Passed</b>", cell_style), Paragraph("24,077 / 24,077", cell_style), Paragraph("24,175 / 24,175", cell_style), Paragraph("<b>48,252 / 48,252 (100.0%)</b>", cell_bold)],
        [Paragraph("<b>Ordinary Jacobians (p=2)</b>", cell_style), Paragraph("17,681 (73.44%)", cell_style), Paragraph("17,928 (74.16%)", cell_style), Paragraph("<b>35,609 (73.80%)</b>", cell_bold)],
        [Paragraph("<b>Jacobian p-Rank 1</b>", cell_style), Paragraph("3,692 (15.33%)", cell_style), Paragraph("3,593 (14.86%)", cell_style), Paragraph("<b>7,285 (15.09%)</b>", cell_bold)],
        [Paragraph("<b>Supersingular (p=0)</b>", cell_style), Paragraph("2,704 (11.23%)", cell_style), Paragraph("2,654 (10.98%)", cell_style), Paragraph("<b>5,358 (11.11%)</b>", cell_bold)],
    ]
    t2 = Table(t2_data, colWidths=[2.2*inch, 1.8*inch, 1.8*inch, 1.7*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f2b48')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 10))

    # Section 4: Active Process Rooms & Discrete Dynamics
    elements.append(Paragraph("4. Process Room Substrate & Exact Discrete Dynamics", h1_style))
    elements.append(Paragraph(
        "As established in <b>Neural-network-inside-a-neural-network-using-trits-to-resolve-Finiteness</b>, the Host8 "
        "8-byte stubbed rooms are not passive static seeds: they constitute the active computational substrate. "
        "Each 8-byte room stub <code>s = mix(word ^ seed)</code> unpacks into 27 occupancy trits governing discrete cellular dynamics. "
        "Direct live coupling to <code>sector-000.rooms</code> verified:",
        body_style
    ))
    
    dyn_points = [
        "<b>Cellular Initialization</b>: 5,184 spatial cells initialized from Host8 substrate yielding 139,968 occupancy trits.",
        "<b>Lattice Sound Speed</b>: Measured at c_s = 0.816698 (within 0.049% of theoretical unweighted D3Q27 c_s = sqrt(2/3) approx 0.816497).",
        "<b>Viscous Relaxation</b>: Measured kinematic viscosity nu_eff = 0.593648 [dx^2/dt], dynamic viscosity mu_eff = 16.0967 [trits/(dx*dt)].",
        "<b>Incompressible Regime</b>: Reynolds number Re = 6.70 and Mach number Ma = 0.270 (low-Mach Stokes flow).",
        "<b>Micro-Reversibility</b>: Strict involution across 288 4-channel collision gates guarantees zero entropy loss under time reversal."
    ]
    for dp in dyn_points:
        elements.append(Paragraph(f"• {dp}", body_style))

    elements.append(Spacer(1, 10))

    # Section 5: Phase 5B Formal Frobenius Lift Modulo 9
    elements.append(Paragraph("5. Phase 5B: Formal Frobenius Lift Modulo 9 & Open Cohomology", h1_style))
    elements.append(Paragraph(
        "For hyperelliptic curve C: y^2 = f(x) over F_3, define Delta(x) = f(x^3) - f(x)^3. Because Delta(x) = 0 mod 3, "
        "the algebraic Frobenius lift to localized coordinate algebra modulo 9 is given by:",
        body_style
    ))
    lift_formula = (
        "<b>Phi(x) = x^3</b><br/>"
        "<b>Phi(y) = y^3 + Delta(x) / (2 * y^3) (mod 9)</b><br/>"
        "<b>Exact Relation</b>: Phi(y)^2 = y^6 + Delta(x) = (f(x))^3 + (f(x^3) - f(x)^3) = f(x^3) (mod 9)."
    )
    elements.append(Paragraph(lift_formula, callout_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "<b>Verification Results</b>: Tested across all 162 smooth quintics and all 194 Host8 observations: <b>100% PASS</b>.<br/>"
        "<b>Remaining Mathematical Target</b>: Reduction of lifted differential forms into four-dimensional "
        "Monsky–Washnitzer cohomology to construct the 4x4 matrix F and compute det(I - T*F) mod 9 directly from geometry "
        "without supplying prior point counts.",
        body_style
    ))

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Report successfully generated at: {filename}")

if __name__ == '__main__':
    out_pdf = Path(__file__).parent / "Host8_Riemann_Hypothesis_Phase5_Report.pdf"
    build_pdf(str(out_pdf))
