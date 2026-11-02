import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def update_document():
    doc = docx.Document("AI_Project_File (1).docx.bak")

    # ================= 1. UPDATE TABLE 0 (INDEX) =================
    table0 = doc.tables[0]
    
    # Target rows data
    toc_data = [
        ("Chapter No.", "Title", "Page No.*"),
        ("—", "Declaration", "i"),
        ("—", "Acknowledgement", "ii"),
        ("—", "Introduction", "iii"),
        ("1", "Objective, Relevance and Scope", "1"),
        ("1.1", "Objective of the Project", "1"),
        ("1.2", "Relevance of the Project", "2"),
        ("1.3", "Scope of the Project", "3"),
        ("2", "Literature Survey and Existing System", "4"),
        ("2.1", "Literature Survey", "4"),
        ("2.2", "Existing System", "5"),
        ("3", "Algorithm Used and Dataset Source", "6"),
        ("3.1", "AI Algorithm Used and Justification", "6"),
        ("3.2", "Mathematical Formulation of the Timetable CSP", "7"),
        ("3.3", "Step-by-Step Algorithms and Pseudocode", "8"),
        ("3.4", "Dataset Source", "11"),
        ("4", "Methodology and Input/Output Constraints", "12"),
        ("4.1", "Methodology and Workflow", "12"),
        ("4.2", "Input Constraints", "13"),
        ("4.3", "Output Constraints", "15"),
        ("5", "Hardware and Software Requirements", "17"),
        ("5.1", "Hardware Requirements", "17"),
        ("5.2", "Software Requirements", "18"),
        ("6", "Code Output and Design", "19"),
        ("6.1", "Code Quality and Modular Design", "19"),
        ("6.2", "Program Execution and Results", "20"),
        ("6.3", "Performance Evaluation Metrics", "24"),
        ("6.4", "Working of the Algorithm and Observations", "25"),
        ("7", "Time and Space Complexity", "26"),
        ("7.1", "Time Complexity Analysis", "26"),
        ("7.2", "Space Complexity Analysis", "28"),
        ("8", "Features and Future Scope", "29"),
        ("8.1", "Key Features of the Project", "29"),
        ("8.2", "Future Scope", "30"),
        ("8.3", "Future Enhancements", "30"),
        ("9", "Innovation and Conclusion", "31"),
        ("9.1", "Innovation and Additional Features", "31"),
        ("9.2", "Conclusion", "31"),
        ("10", "References", "32"),
    ]

    # Adjust row count of table0
    while len(table0.rows) < len(toc_data):
        table0.add_row()
    while len(table0.rows) > len(toc_data):
        table0._tbl.remove(table0.rows[-1]._tr)

    for idx, (ch, title, page) in enumerate(toc_data):
        row = table0.rows[idx]
        cells = row.cells
        cells[0].text = ch
        cells[1].text = title
        cells[2].text = page
        
        is_header = (idx == 0)
        is_major = not ('.' in ch) and ch != "—" and not is_header

        for col_idx, c in enumerate(cells):
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            if is_header:
                set_cell_background(c, "1B365D")
                if p.runs:
                    p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    p.runs[0].font.bold = True
            elif is_major:
                set_cell_background(c, "EAEFF5")
                if p.runs:
                    p.runs[0].font.bold = True
            else:
                set_cell_background(c, "F9FAFB" if idx % 2 == 1 else "FFFFFF")

    # ================= 2. INSERT ALGORITHMS INTO CHAPTER 3 =================
    # Find paragraph "3.2 Dataset Source"
    target_idx = None
    for i, p in enumerate(doc.paragraphs):
        if "3.2 Dataset Source" in p.text:
            target_idx = i
            break

    print(f"Target index for 3.2 Dataset Source: {target_idx}")
    if target_idx is not None:
        p_target = doc.paragraphs[target_idx]

        def insert_p(text, bold=False, italic=False, size_pt=11.5, space_after=6, font_name="Times New Roman"):
            new_p = p_target.insert_paragraph_before()
            new_p.paragraph_format.space_after = Pt(space_after)
            new_p.paragraph_format.line_spacing = 1.15
            run = new_p.add_run(text)
            run.font.name = font_name
            run.font.size = Pt(size_pt)
            run.bold = bold
            run.italic = italic
            return new_p

        def insert_heading(text, level=2):
            size = 13 if level == 2 else 12
            return insert_p(text, bold=True, size_pt=size, space_after=4)

        def insert_code(code_str):
            new_p = p_target.insert_paragraph_before()
            new_p.paragraph_format.space_before = Pt(4)
            new_p.paragraph_format.space_after = Pt(8)
            new_p.paragraph_format.left_indent = Inches(0.2)
            run = new_p.add_run(code_str)
            run.font.name = "Courier New"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0x22, 0x33, 0x44)
            return new_p

        # Section 3.2: Mathematical Formulation
        insert_heading("3.2 Mathematical Formulation of the Timetable CSP", level=2)
        insert_p(
            "A standard Constraint Satisfaction Problem (CSP) for academic timetabling is formally "
            "defined as a 3-tuple <X, D, C> where:"
        )
        insert_p(
            "1. Variables (X):\n"
            "Each course c requires S_c sessions per week. Each individual session is modeled as an "
            "independent decision variable:\n"
            "   X = { X_{c, k} | c ∈ Courses, 1 ≤ k ≤ S_c }\n"
            "The total number of variables is n = |X| = ∑ S_c."
        )
        insert_p(
            "2. Domains (D):\n"
            "The domain D(X_{c, k}) represents the set of all valid triples (room, day, period) that "
            "satisfy initial physical constraints:\n"
            "   D(X_{c, k}) = { (r, d, p) | r ∈ Rooms, d ∈ Days, p ∈ Periods }\n"
            "subject to:\n"
            "   • Room Capacity: Capacity(r) ≥ Students(c)\n"
            "   • Room Type: Type(r) == Type(c) (Classroom vs. Laboratory)"
        )
        insert_p(
            "3. Hard Constraints (C_hard):\n"
            "Every valid schedule must satisfy the following zero-tolerance hard constraints:\n"
            "   • Teacher Clash: No faculty member can be assigned to multiple sessions at the same (day, period).\n"
            "     ∀ X_i, X_j (i ≠ j): Teacher(X_i) == Teacher(X_j) ⟹ (d_i, p_i) ≠ (d_j, p_j)\n"
            "   • Section Clash: A student section cannot attend two simultaneous lectures.\n"
            "     ∀ X_i, X_j (i ≠ j): Section(X_i) == Section(X_j) ⟹ (d_i, p_i) ≠ (d_j, p_j)\n"
            "   • Room Clash: A room cannot host more than one session at the same time.\n"
            "     ∀ X_i, X_j (i ≠ j): r_i == r_j ⟹ (d_i, p_i) ≠ (d_j, p_j)\n"
            "   • Daily Distribution: Multiple sessions of the same course must be allocated on distinct days.\n"
            "     ∀ X_i, X_j (i ≠ j): Course(X_i) == Course(X_j) ⟹ d_i ≠ d_j"
        )
        insert_p(
            "4. Soft Constraints & Scoring Function (C_soft):\n"
            "To maximize timetable quality and pedagogical effectiveness, the system minimizes a weighted penalty:\n"
            "   Penalty = 3 × (Empty Periods) + 5 × (Consecutive Difficult) + 2 × (Faculty Violations) + 2 × (Distribution Penalty)\n"
            "   Quality Score = max(0, 100 - Penalty)"
        )

        # Section 3.3: Step-by-Step Algorithms and Pseudocode
        insert_heading("3.3 Step-by-Step Algorithms and Pseudocode", level=2)
        insert_p(
            "The timetable generation engine employs four distinct algorithms working in harmony to enforce hard "
            "constraints and optimize soft constraints:"
        )

        insert_heading("Algorithm 1: Variable and Domain Initialization", level=3)
        insert_code(
            "Algorithm: INITIALIZE_CSP(Courses, Rooms, Days, Periods)\n"
            "Input: Course catalog, Available rooms, Working days, Daily periods\n"
            "Output: Variable set X, Initial domains D\n\n"
            "1:  X ← Empty Dictionary\n"
            "2:  For each course c in Courses:\n"
            "3:      For session_num ← 1 to c.sessions_per_week:\n"
            "4:          var_name ← c.name + '_' + session_num\n"
            "5:          X[var_name] ← {course: c.name, teacher: c.teacher,\n"
            "                           section: c.section, room_type: c.room_type,\n"
            "                           students: c.students, difficulty: c.difficulty}\n"
            "6:  D ← Empty Dictionary\n"
            "7:  For each var in X:\n"
            "8:      valid_triples ← Empty List\n"
            "9:      For each room r in Rooms:\n"
            "10:         If r.capacity < X[var].students Then Continue\n"
            "11:         If r.type ≠ X[var].room_type Then Continue\n"
            "12:         For each day d in Days:\n"
            "13:             For each period p in Periods:\n"
            "14:                 valid_triples.APPEND((r, d, p))\n"
            "15:     D[var] ← valid_triples\n"
            "16: Return X, D"
        )

        insert_heading("Algorithm 2: Variable Selection Heuristic (MRV + Degree Heuristic)", level=3)
        insert_code(
            "Algorithm: SELECT_UNASSIGNED_VARIABLE(Unassigned, Domains, Timetable, Variables)\n"
            "Input: List of unassigned variables, current domains, partial timetable\n"
            "Output: Next candidate variable to assign\n\n"
            "1:  Candidates ← [v for v in Unassigned if v not in Timetable]\n"
            "2:  If Candidates is empty Then Return NULL\n"
            "3:  Function DEGREE(v):\n"
            "4:      count ← 0\n"
            "5:      For each other in Candidates (other ≠ v):\n"
            "6:          If Variables[v].teacher == Variables[other].teacher OR\n"
            "             Variables[v].section == Variables[other].section Then:\n"
            "              count ← count + 1\n"
            "7:      Return count\n"
            "8:  BestVariable ← argmin_{v ∈ Candidates} ( |Domains[v]|, -DEGREE(v) )\n"
            "9:  Return BestVariable"
        )

        insert_heading("Algorithm 3: Backtracking Search with Forward Checking (FC-MRV)", level=3)
        insert_code(
            "Algorithm: BACKTRACKING_SEARCH(Variables, Domains, Timetable, Rooms, Nodes)\n"
            "Input: Variables X, Domains D, Partial assignment Timetable, Rooms, Nodes\n"
            "Output: Conflict-free Timetable or NULL\n\n"
            "1:  If |Timetable| == |Variables| Then Return Copy(Timetable)\n"
            "2:  var ← SELECT_UNASSIGNED_VARIABLE(Variables, Domains, Timetable, Variables)\n"
            "3:  If var is NULL Then Return NULL\n"
            "4:  For each assignment (r, d, p) in Copy(Domains[var]):\n"
            "5:      Nodes[0] ← Nodes[0] + 1\n"
            "6:      If NOT IS_VALID_ASSIGNMENT(var, r, d, p, Timetable, Variables, Rooms) Then Continue\n"
            "7:      Timetable[var] ← (r, d, p)\n"
            "8:      SavedDomains ← Empty Map, ForwardCheckPassed ← True\n"
            "9:      For each unassigned_var in Variables \\ Timetable:\n"
            "10:         SavedDomains[unassigned_var] ← Copy(Domains[unassigned_var])\n"
            "11:         PrunedDomain ← Filter(Domains[unassigned_var], IS_VALID_ASSIGNMENT)\n"
            "12:         Domains[unassigned_var] ← PrunedDomain\n"
            "13:         If |PrunedDomain| == 0 Then:\n"
            "14:             ForwardCheckPassed ← False; Break\n"
            "15:     If ForwardCheckPassed Then:\n"
            "16:         result ← BACKTRACKING_SEARCH(Variables, Domains, Timetable, Rooms, Nodes)\n"
            "17:         If result ≠ NULL Then Return result\n"
            "18:     Delete Timetable[var]\n"
            "19:     For each (u, orig_domain) in SavedDomains: Domains[u] ← orig_domain\n"
            "20: Return NULL"
        )

        insert_heading("Algorithm 4: Multi-Attempt Stochastic Optimization Algorithm", level=3)
        insert_code(
            "Algorithm: GENERATE_OPTIMIZED_TIMETABLE(Courses, Rooms, Days, Periods, Preferences, Attempts)\n"
            "Input: Academic data, faculty preferences, number of attempts\n"
            "Output: Optimal timetable with maximum quality score\n\n"
            "1:  Variables, BaseDomains ← INITIALIZE_CSP(Courses, Rooms, Days, Periods)\n"
            "2:  BestTimetable ← NULL, BestPenalty ← ∞, BestMetrics ← NULL\n"
            "3:  For attempt ← 1 to Attempts:\n"
            "4:      Domains ← Copy(BaseDomains)\n"
            "5:      For each var in Domains: SHUFFLE(Domains[var])\n"
            "6:      Timetable ← BACKTRACKING_SEARCH(Variables, Domains, Empty, Rooms, [0])\n"
            "7:      If Timetable is NULL Then Continue\n"
            "8:      Metrics ← EVALUATE_TIMETABLE(Timetable, Variables, Preferences, Periods)\n"
            "9:      If Metrics.total_penalty < BestPenalty Then:\n"
            "10:         BestTimetable ← Copy(Timetable)\n"
            "11:         BestPenalty ← Metrics.total_penalty; BestMetrics ← Metrics\n"
            "12:     If BestPenalty == 0 Then Break\n"
            "13: Return BestTimetable, BestMetrics"
        )

    # Change "3.2 Dataset Source" to "3.4 Dataset Source"
    for p in doc.paragraphs:
        if "3.2 Dataset Source" in p.text:
            p.text = p.text.replace("3.2 Dataset Source", "3.4 Dataset Source")

    # ================= 3. HARMONIZE CHAPTER HEADINGS =================
    # Insert "Chapter 4: Methodology and Input/Output Constraints" before 4.1 Methodology
    for p in doc.paragraphs:
        if p.text.strip() == "4.1 Methodology and Workflow":
            new_h1 = p.insert_paragraph_before("Chapter 4: Methodology and Input/Output Constraints", style='Heading 1')
            new_h1.paragraph_format.space_before = Pt(16)
            new_h1.paragraph_format.space_after = Pt(6)
            break

    # Renumber subsequent chapter headings
    replacements = [
        ("Chapter 4: Hardware and Software Requirements", "Chapter 5: Hardware and Software Requirements"),
        ("4.1 Hardware Requirements", "5.1 Hardware Requirements"),
        ("4.2 Software Requirements", "5.2 Software Requirements"),
        ("Chapter 5: Code Output and Design", "Chapter 6: Code Output and Design"),
        ("5.1 Code Quality and Modular Design", "6.1 Code Quality and Modular Design"),
        ("5.2 Program Execution and Results", "6.2 Program Execution and Results"),
        ("5.3 Performance Evaluation Metrics", "6.3 Performance Evaluation Metrics"),
        ("5.4 Working of the Algorithm and Observations", "6.4 Working of the Algorithm and Observations"),
        ("Chapter 6: Time and Space Complexity", "Chapter 7: Time and Space Complexity"),
        ("6.1 Time Complexity Analysis", "7.1 Time Complexity Analysis"),
        ("6.2 Space Complexity Analysis", "7.2 Space Complexity Analysis"),
        ("Chapter 7: Features and Future Scope", "Chapter 8: Features and Future Scope"),
        ("7.1 Key Features of the Project", "8.1 Key Features of the Project"),
        ("7.2 Future Scope", "8.2 Future Scope"),
        ("7.3 Future Enhancements", "8.3 Future Enhancements"),
        ("Chapter 8: Features and Conclusion", "Chapter 9: Innovation and Conclusion"),
        ("8.1 Innovation and Additional Features", "9.1 Innovation and Additional Features"),
        ("8.2 Conclusion", "9.2 Conclusion"),
        ("Chapter 9: References", "Chapter 10: References"),
    ]

    for p in doc.paragraphs:
        txt = p.text.strip()
        for old_t, new_t in replacements:
            if txt == old_t:
                p.text = new_t

    # Save to all target paths
    out1 = "AI_University_Timetable_Generator_Project_Report.docx"
    out2 = "PROJECT_REPORT.docx"
    out3 = "AI_Project_File (1).docx"

    doc.save(out1)
    doc.save(out2)
    doc.save(out3)
    print("Updated docx successfully saved to:")
    print(" -", out1)
    print(" -", out2)
    print(" -", out3)

if __name__ == "__main__":
    update_document()
