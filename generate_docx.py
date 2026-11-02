import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
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

def create_report_docx():
    doc = Document()

    # Set margins to 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11.5)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(6)

    # Colors
    NAVY = RGBColor(0x1B, 0x36, 0x5D)
    SLATE = RGBColor(0x33, 0x4E, 0x68)
    BLACK = RGBColor(0x11, 0x11, 0x11)
    MUTED = RGBColor(0x55, 0x55, 0x55)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(20)
        run.font.color.rgb = NAVY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = BLACK
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(15)
        run.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = SLATE
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = BLACK
        return p

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.2
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
        run = p.add_run(text)
        run.italic = italic
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
        p.add_run(text)
        return p

    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F4F6F8")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        run = p.add_run(code_text)
        run.font.name = 'Courier New'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        doc.add_paragraph() # small spacing

    # ==================== COVER / TITLE PAGE ====================
    add_title("PROJECT REPORT (CSN304)")
    add_subtitle("A report submitted in partial fulfilment of the requirement for the course")
    
    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_course.add_run("ARTIFICIAL INTELLIGENCE")
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = NAVY

    add_subtitle("Part of the degree of\nBACHELOR OF TECHNOLOGY\nCOMPUTER SCIENCE AND ENGINEERING")

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(10)
    p_div.paragraph_format.space_after = Pt(10)
    r_dit = p_div.add_run("DIT UNIVERSITY\nIMAGINE • ASPIRE • ACHIEVE")
    r_dit.bold = True
    r_dit.font.size = Pt(16)
    r_dit.font.color.rgb = NAVY

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(16)
    p_meta.paragraph_format.space_after = Pt(6)
    r_fac = p_meta.add_run("Submitted to Faculty Name: ")
    r_fac.bold = True
    p_meta.add_run("Dr. Himani Sharma\nAssistant Professor\n\n")
    
    r_sub = p_meta.add_run("Submitted by:\n")
    r_sub.bold = True
    p_meta.add_run(
        "• Names: Utkarsh Goswami, Aryan Chettri, Mohammad Ariz Khan\n"
        "• Roll Nos: 24A04D1813, 24A03A0205, 24A04D0801\n"
        "• SAP IDs: 1000026654, 1000026710, 1000026616\n"
        "• Section: I (P2)\n\n"
    )

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    r_sch = p_inst.add_run("SCHOOL OF COMPUTING\nDIT UNIVERSITY, DEHRADUN\n")
    r_sch.bold = True
    r_sch.font.size = Pt(13)
    r_sch.font.color.rgb = NAVY
    p_inst.add_run(
        "(State Private University through State Legislature Act No. 10 of 2013 of Uttarakhand and approved by UGC)\n"
        "Mussoorie Diversion Road, Dehradun, Uttarakhand - 248009, India.\n"
        "November 2026"
    )

    doc.add_page_break()

    # ==================== DECLARATION ====================
    add_h1("Declaration")
    add_p(
        "I hereby certify that the work, which is being presented in the Report, entitled "
        "“AI-Based University Timetable Generator”, in partial fulfilment of the requirement "
        "as part of the course Bachelor of Technology and submitted to DIT University is an "
        "authentic record of our work carried out during the period 12/10/2026 to 26/10/2026 "
        "under the guidance of Dr. Himani Sharma."
    )

    tbl_dec = doc.add_table(rows=4, cols=2)
    tbl_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl_dec.rows[0].cells
    hdr[0].text = "Name of the Student"
    hdr[1].text = "Signature and Date"
    for c in hdr:
        set_cell_background(c, "1B365D")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].bold = True
        set_cell_margins(c, top=100, bottom=100, left=150, right=150)

    names = ["Utkarsh Goswami", "Aryan Chettri", "Mohammad Ariz Khan"]
    for i, name in enumerate(names, start=1):
        row = tbl_dec.rows[i].cells
        row[0].text = name
        row[1].text = "_________________________"
        for c in row:
            set_cell_margins(c, top=100, bottom=100, left=150, right=150)
            set_cell_background(c, "F9FAFB" if i % 2 == 1 else "FFFFFF")

    doc.add_paragraph() # spacing

    # ==================== ACKNOWLEDGEMENT ====================
    add_h1("Acknowledgement")
    add_p(
        "We are sincerely grateful to all who have supported us in this project. First, we extend our "
        "heartfelt thanks to our project guide, Dr. Himani Sharma, for her invaluable guidance, "
        "dedication, and encouragement throughout this endeavor. Her expertise and thoughtful insights "
        "were instrumental in shaping our progress."
    )
    add_p(
        "We also thank each member of our team, whose hard work, collaboration, and commitment made "
        "this project possible. Your support has been invaluable, and we deeply appreciate your efforts."
    )
    add_p("Thank you all for helping make this project a success.")
    add_p("• Utkarsh Goswami\n• Aryan Chettri\n• Mohammad Ariz Khan")

    doc.add_page_break()

    # ==================== TABLE OF CONTENT ====================
    add_h1("TABLE OF CONTENT")
    
    toc_data = [
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

    tbl_toc = doc.add_table(rows=len(toc_data) + 1, cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # TOC Header
    th = tbl_toc.rows[0].cells
    th[0].text = "Chapter No."
    th[1].text = "Title"
    th[2].text = "Page No."
    for c in th:
        set_cell_background(c, "1B365D")
        run = c.paragraphs[0].runs[0]
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.bold = True
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)

    # Set column widths
    tbl_toc.columns[0].width = Inches(1.3)
    tbl_toc.columns[1].width = Inches(4.3)
    tbl_toc.columns[2].width = Inches(0.9)

    for idx, (ch_num, title, page) in enumerate(toc_data, start=1):
        row = tbl_toc.rows[idx].cells
        row[0].text = ch_num
        row[1].text = title
        row[2].text = page
        
        is_major = not ('.' in ch_num) and ch_num != "—"
        for i_col, c in enumerate(row):
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            if is_major:
                set_cell_background(c, "EAEFF5")
                c.paragraphs[0].runs[0].bold = True
            elif idx % 2 == 1:
                set_cell_background(c, "F9FAFB")

    doc.add_page_break()

    # ==================== INTRODUCTION ====================
    add_h1("Introduction")
    add_p(
        "In modern educational institutions, creating an academic timetable is one of the most "
        "complex and time-consuming administrative tasks. Universities must allocate courses, "
        "faculty members, classrooms, laboratories, student groups, and time slots while ensuring "
        "that no scheduling conflicts occur. As the number of courses and academic resources increases, "
        "manual timetable preparation becomes increasingly difficult, often resulting in teacher clashes, "
        "student section overlaps, inefficient room utilization, and frequent timetable revisions. These "
        "challenges not only increase administrative workload but also affect the overall academic "
        "experience of students and faculty members."
    )
    add_p(
        "Artificial Intelligence (AI) provides an effective solution for addressing such scheduling "
        "problems through intelligent decision-making and optimization techniques. Timetable generation "
        "can be modeled as a Constraint Satisfaction Problem (CSP), where various academic entities must "
        "be assigned appropriate values while satisfying predefined constraints. By utilizing CSP-based "
        "techniques, institutions can automate the scheduling process and generate conflict-free timetables "
        "efficiently. The use of AI eliminates repetitive manual effort, reduces errors, optimizes resource "
        "allocation, and enables institutions to respond quickly to changes in academic requirements."
    )
    add_p(
        "The AI-Based University Timetable Generator developed in this project applies advanced CSP "
        "techniques such as Backtracking Search, Minimum Remaining Values (MRV), Degree Heuristic, and "
        "Forward Checking to generate optimized weekly schedules. The system enforces both hard constraints "
        "and soft constraints to ensure not only timetable correctness but also timetable quality. Through "
        "an interactive Streamlit-based interface, users can generate, analyze, validate, and compare "
        "timetables using various performance metrics. This project demonstrates the practical application "
        "of Artificial Intelligence in solving a real-world scheduling problem and highlights how intelligent "
        "systems can improve efficiency in educational administration."
    )

    doc.add_page_break()

    # ==================== CHAPTER 1 ====================
    add_h1("Chapter 1: Objective, Relevance and Scope")
    
    add_h2("1.1 Objective of the Project")
    add_p(
        "The primary objective of this project is to design and develop an AI-Based University Timetable "
        "Generator that can automatically create optimized academic schedules while satisfying institutional "
        "constraints. The system aims to eliminate scheduling conflicts related to teachers, student sections, "
        "classrooms, and laboratory facilities. It also seeks to improve scheduling efficiency by reducing manual "
        "effort, minimizing resource wastage, and producing balanced timetables that meet academic requirements."
    )
    add_p(
        "Another key objective is to implement intelligent optimization techniques that improve timetable "
        "quality. The system evaluates generated schedules based on soft constraints such as faculty "
        "preferences, course distribution, minimization of empty periods, and avoidance of consecutive "
        "difficult subjects. By automating the scheduling process, the project provides a reliable and scalable "
        "solution for academic institutions."
    )

    add_h2("1.2 Relevance of the Project")
    add_p(
        "Timetable scheduling is a critical function in educational institutions because it directly affects "
        "students, faculty members, and administrative operations. Traditional scheduling methods often require "
        "considerable time and effort while still being susceptible to conflicts and inefficiencies. As "
        "universities continue to expand, managing increasing numbers of courses, classrooms, and faculty "
        "members through manual processes becomes impractical."
    )
    add_p(
        "This project is highly relevant because it demonstrates how Artificial Intelligence can be applied "
        "to solve a common real-world problem effectively. By utilizing CSP-based optimization, the system "
        "generates conflict-free schedules while maximizing resource utilization. The intelligent scheduling "
        "process reduces administrative burden, enhances academic planning, and provides educational institutions "
        "with a modern solution capable of adapting to changing requirements."
    )

    add_h2("1.3 Scope of the Project")
    add_p(
        "The scope of this project includes the generation of university timetables involving courses, faculty "
        "members, student sections, classrooms, laboratory facilities, working days, and available periods. The "
        "system is capable of creating complete weekly schedules while ensuring compliance with all hard constraints."
    )
    add_p(
        "In addition to basic timetable generation, the project evaluates and optimizes timetable quality through "
        "various soft constraints. The modular architecture allows future expansion to support multiple departments, "
        "larger datasets, cloud deployment, mobile applications, centralized academic databases, and web-based "
        "scheduling systems. The project provides a strong foundation for developing enterprise-level university "
        "scheduling solutions."
    )

    doc.add_page_break()

    # ==================== CHAPTER 2 ====================
    add_h1("Chapter 2: Literature Survey and Existing System")
    
    add_h2("2.1 Literature Survey")
    add_p(
        "University timetable scheduling has been widely studied in the fields of Artificial Intelligence, "
        "Optimization, and Operations Research. Earlier timetable generation methods relied heavily on manual "
        "scheduling processes and spreadsheet-based systems. Although these methods provided a basic solution, "
        "they were inefficient and prone to human errors."
    )
    add_p(
        "Researchers have proposed several optimization approaches such as Constraint Satisfaction Problems (CSP), "
        "Genetic Algorithms (GA), Simulated Annealing (SA), Tabu Search, and Ant Colony Optimization. Among these, "
        "CSP has emerged as one of the most effective techniques because it directly represents scheduling "
        "requirements as constraints that must be satisfied. The CSP approach guarantees valid solutions and "
        "provides a structured framework for handling complex scheduling requirements."
    )
    add_p(
        "Recent research emphasizes the use of heuristic techniques such as Minimum Remaining Values (MRV), Degree "
        "Heuristic, and Forward Checking to improve CSP efficiency. These methods reduce computational effort and "
        "improve scalability by minimizing unnecessary search operations. The present project adopts a CSP-based "
        "methodology because it combines reliability, flexibility, and optimization capabilities, making it highly "
        "suitable for university timetable generation."
    )

    add_h2("2.2 Existing System")
    add_p(
        "Most educational institutions still rely on manually prepared timetables or semi-automated spreadsheet "
        "systems. In such systems, administrators assign courses to rooms and time slots based on experience and "
        "institutional guidelines. While these approaches may work for small datasets, they become increasingly "
        "difficult to manage as the number of courses, student groups, and faculty members grows."
    )
    add_p(
        "Existing scheduling systems often focus only on satisfying basic constraints and may neglect optimization "
        "requirements such as faculty preferences, balanced workloads, and efficient resource utilization. As a "
        "result, generated timetables frequently require manual adjustments. These limitations create the need for "
        "an intelligent scheduling solution capable of generating conflict-free and optimized timetables automatically."
    )

    doc.add_page_break()

    # ==================== CHAPTER 3 ====================
    add_h1("Chapter 3: Algorithm Used and Dataset Source")
    
    add_h2("3.1 AI Algorithm Used and Justification")
    add_p(
        "This project employs a Constraint Satisfaction Problem (CSP) approach enhanced by Backtracking Search, "
        "Minimum Remaining Values (MRV) Heuristic, Degree Heuristic, and Forward Checking, coupled with a "
        "Multi-Attempt Stochastic Optimizer. CSP is particularly suitable because timetable generation involves "
        "assigning values to discrete variables while satisfying strict hard constraints and optimizing soft constraints."
    )
    add_p(
        "Backtracking Search systematically explores possible assignments until a valid solution is found. The MRV "
        "heuristic selects the most constrained variable first, thereby drastically pruning the search space. The "
        "Degree Heuristic prioritizes variables connected to the largest number of constraints to break ties, while "
        "Forward Checking proactively eliminates invalid future choices from unassigned domains. These techniques "
        "collectively improve execution efficiency and enable the solver to generate valid schedules in milliseconds."
    )
    add_p(
        "The chosen AI approach is more appropriate than classification or deep-learning models because timetable "
        "generation is fundamentally a constraint optimization and combinatorial search problem rather than a "
        "pattern recognition problem. Therefore, CSP provides mathematical correctness, zero conflict guarantee, "
        "and flexible optimization capabilities."
    )

    add_h2("3.2 Mathematical Formulation of the Timetable CSP")
    add_p("A standard Constraint Satisfaction Problem is formally defined as a 3-tuple <X, D, C>:")
    
    add_p(
        "1. Variables (X):\n"
        "Each course c in Courses requires a specific number of weekly sessions S_c. Each session is modeled as an "
        "independent scheduling variable:\n"
        "   X = { X_{c, k} | c in Courses, 1 <= k <= S_c }\n"
        "where n = |X| = sum(S_c) represents the total number of sessions to schedule."
    )
    add_p(
        "2. Domains (D):\n"
        "The domain D(X_{c, k}) represents the set of all valid triples (room, day, period) satisfying initial capacity "
        "and room-type filters:\n"
        "   D(X_{c, k}) = { (r, d, p) | r in Rooms, d in Days, p in Periods }\n"
        "subject to:\n"
        "   • Capacity(r) >= Students(c)\n"
        "   • Type(r) == Type(c) (Classroom vs. Laboratory)"
    )
    add_p(
        "3. Hard Constraints (C_hard):\n"
        "An assignment A: X -> D is valid if and only if all hard constraints are satisfied:\n"
        "   • Teacher Clash: No teacher can teach multiple classes simultaneously.\n"
        "     For all X_i, X_j (i != j): Teacher(X_i) == Teacher(X_j) => (d_i, p_i) != (d_j, p_j)\n"
        "   • Section Clash: A student section cannot attend two classes at the same time.\n"
        "     For all X_i, X_j (i != j): Section(X_i) == Section(X_j) => (d_i, p_i) != (d_j, p_j)\n"
        "   • Room Clash: A room cannot host two distinct sessions simultaneously.\n"
        "     For all X_i, X_j (i != j): r_i == r_j => (d_i, p_i) != (d_j, p_j)\n"
        "   • Daily Frequency: Repeated sessions of the same course must occur on distinct days.\n"
        "     For all X_i, X_j (i != j): Course(X_i) == Course(X_j) => d_i != d_j"
    )
    add_p(
        "4. Soft Constraints & Quality Scoring Function (C_soft):\n"
        "Among conflict-free solutions, the system minimizes the total penalty score:\n"
        "   Penalty = 3 * (Empty Periods) + 5 * (Consecutive Difficult) + 2 * (Faculty Violations) + 2 * (Course Distribution Penalty)\n\n"
        "The overall Quality Score (0 to 100) is evaluated as:\n"
        "   Quality Score = max(0, 100 - Penalty)"
    )

    add_h2("3.3 Step-by-Step Algorithms and Pseudocode")
    add_p("The timetable scheduling engine is organized into four core algorithms:")

    add_h3("Algorithm 1: Variable and Domain Initialization")
    add_code_block(
        "Algorithm: INITIALIZE_CSP(Courses, Rooms, Days, Periods)\n"
        "Input: Course catalog, Available rooms, Working days, Daily periods\n"
        "Output: Variable set X, Initial domains D\n\n"
        "1:  X <- Empty Dictionary\n"
        "2:  For each course c in Courses:\n"
        "3:      For session_num <- 1 to c.sessions_per_week:\n"
        "4:          var_name <- c.name + '_' + session_num\n"
        "5:          X[var_name] <- {course: c.name, teacher: c.teacher,\n"
        "                           section: c.section, room_type: c.room_type,\n"
        "                           students: c.students, difficulty: c.difficulty}\n"
        "6:  D <- Empty Dictionary\n"
        "7:  For each var in X:\n"
        "8:      valid_triples <- Empty List\n"
        "9:      For each room r in Rooms:\n"
        "10:         If r.capacity < X[var].students Then Continue\n"
        "11:         If r.type != X[var].room_type Then Continue\n"
        "12:         For each day d in Days:\n"
        "13:             For each period p in Periods:\n"
        "14:                 valid_triples.APPEND((r, d, p))\n"
        "15:     D[var] <- valid_triples\n"
        "16: Return X, D"
    )

    add_h3("Algorithm 2: Variable Selection Heuristic (MRV with Degree Heuristic)")
    add_code_block(
        "Algorithm: SELECT_UNASSIGNED_VARIABLE(Unassigned, Domains, Timetable, Variables)\n"
        "Input: List of unassigned variables, current variable domains, partial timetable\n"
        "Output: The best candidate variable to assign next\n\n"
        "1:  Candidates <- [v for v in Unassigned if v not in Timetable]\n"
        "2:  If Candidates is empty Then Return NULL\n"
        "3:  Function DEGREE(v):\n"
        "4:      count <- 0\n"
        "5:      For each other in Candidates (other != v):\n"
        "6:          If Variables[v].teacher == Variables[other].teacher OR\n"
        "             Variables[v].section == Variables[other].section Then:\n"
        "              count <- count + 1\n"
        "7:      Return count\n"
        "8:  BestVariable <- argmin_{v in Candidates} ( |Domains[v]|, -DEGREE(v) )\n"
        "9:  Return BestVariable"
    )

    add_h3("Algorithm 3: Backtracking Search with Forward Checking (FC-MRV)")
    add_code_block(
        "Algorithm: BACKTRACKING_SEARCH(Variables, Domains, Timetable, Rooms, Nodes)\n"
        "Input: Variables X, Domains D, Partial assignment Timetable, Rooms, Counter Nodes\n"
        "Output: Conflict-free Timetable or NULL\n\n"
        "1:  If |Timetable| == |Variables| Then:\n"
        "2:      Return Copy(Timetable)                 // Complete valid assignment found\n"
        "3:  var <- SELECT_UNASSIGNED_VARIABLE(Variables, Domains, Timetable, Variables)\n"
        "4:  If var is NULL Then Return NULL\n"
        "5:  For each assignment (r, d, p) in Copy(Domains[var]):\n"
        "6:      Nodes[0] <- Nodes[0] + 1\n"
        "7:      If NOT IS_VALID_ASSIGNMENT(var, r, d, p, Timetable, Variables, Rooms) Then:\n"
        "8:          Continue                           // Hard constraint violated\n"
        "9:      Timetable[var] <- (r, d, p)\n"
        "10:     SavedDomains <- Empty Map\n"
        "11:     ForwardCheckPassed <- True\n"
        "12:     // Forward Checking Phase\n"
        "13:     For each unassigned_var in Variables \\ Timetable:\n"
        "14:         SavedDomains[unassigned_var] <- Copy(Domains[unassigned_var])\n"
        "15:         PrunedDomain <- Filter(Domains[unassigned_var],\n"
        "                                  IS_VALID_ASSIGNMENT against Timetable)\n"
        "16:         Domains[unassigned_var] <- PrunedDomain\n"
        "17:         If |PrunedDomain| == 0 Then:\n"
        "18:             ForwardCheckPassed <- False     // Domain wipe-out detected\n"
        "19:             Break\n"
        "20:     If ForwardCheckPassed Then:\n"
        "21:         result <- BACKTRACKING_SEARCH(Variables, Domains, Timetable, Rooms, Nodes)\n"
        "22:         If result != NULL Then Return result\n"
        "23:     // Backtrack step\n"
        "24:     Delete Timetable[var]\n"
        "25:     For each (u, orig_domain) in SavedDomains:\n"
        "26:         Domains[u] <- orig_domain           // Restore pruned domains\n"
        "27: Return NULL                                // No valid assignment in this branch"
    )

    add_h3("Algorithm 4: Multi-Attempt Stochastic Optimization Algorithm")
    add_code_block(
        "Algorithm: GENERATE_OPTIMIZED_TIMETABLE(Courses, Rooms, Days, Periods, Preferences, Attempts)\n"
        "Input: Academic inputs, faculty preference list, number of search attempts\n"
        "Output: Optimal timetable with maximum quality score\n\n"
        "1:  Variables, BaseDomains <- INITIALIZE_CSP(Courses, Rooms, Days, Periods)\n"
        "2:  BestTimetable <- NULL, BestPenalty <- Infinity, BestMetrics <- NULL\n"
        "3:  For attempt <- 1 to Attempts:\n"
        "4:      Domains <- Copy(BaseDomains)\n"
        "5:      For each var in Domains: SHUFFLE(Domains[var])\n"
        "6:      Timetable <- BACKTRACKING_SEARCH(Variables, Domains, Empty, Rooms, [0])\n"
        "7:      If Timetable is NULL Then Continue\n"
        "8:      Metrics <- EVALUATE_TIMETABLE(Timetable, Variables, Preferences, Periods)\n"
        "9:      If Metrics.total_penalty < BestPenalty Then:\n"
        "10:         BestTimetable <- Copy(Timetable)\n"
        "11:         BestPenalty <- Metrics.total_penalty\n"
        "12:         BestMetrics <- Metrics\n"
        "13:     If BestPenalty == 0 Then Break          // Globally optimal\n"
        "14: Return BestTimetable, BestMetrics"
    )

    add_h2("3.4 Dataset Source")
    add_p(
        "The dataset used in this project is a customized academic scheduling dataset designed specifically "
        "for university timetable generation. It contains information regarding courses, faculty members, "
        "student sections, classrooms, laboratory rooms, room capacities, available time slots, teaching periods, "
        "and faculty preferences."
    )
    add_p(
        "All data is organized using structured Python dictionaries and lists to facilitate efficient processing. "
        "The dataset represents realistic academic scheduling scenarios and can be easily modified to reflect "
        "the requirements of different institutions. Because of its modular design, educational institutions "
        "can replace the sample dataset with their own academic information without altering the core scheduling "
        "algorithm."
    )

    doc.add_page_break()

    # ==================== CHAPTER 4 ====================
    add_h1("Chapter 4: Methodology and Input/Output Constraints")
    
    add_h2("4.1 Methodology and Workflow")
    add_p(
        "The project follows a systematic timetable generation workflow. Initially, academic data is collected "
        "and transformed into CSP variables. Each course session is treated as an independent scheduling "
        "variable requiring assignment to a room, day, and period."
    )
    add_p(
        "The CSP solver generates possible domains for each variable and applies Backtracking Search combined "
        "with MRV, Degree Heuristic, and Forward Checking to identify valid assignments. During the search "
        "process, all hard constraints are continuously verified. If a constraint violation occurs, the solver "
        "immediately backtracks and explores alternative assignments."
    )
    add_p(
        "After generating a valid timetable, a scoring system evaluates timetable quality using soft constraints "
        "such as faculty preferences, empty periods, course distribution, and difficult subject sequencing. The "
        "optimized timetable is then displayed through an interactive Streamlit interface along with performance "
        "statistics and analytical insights."
    )

    add_h2("4.2 Input Constraints")
    add_p(
        "The AI-Based University Timetable Generator requires several input parameters to create a valid and "
        "optimized timetable. These inputs represent the academic resources and scheduling requirements of the "
        "university. The accuracy and completeness of the input data directly affect the quality of the generated "
        "timetable. The system accepts information regarding courses, faculty members, student sections, "
        "classrooms, laboratories, available time slots, and faculty preferences."
    )
    add_p("The timetable generator processes the following input constraints:")

    add_bullet("Course Name, Course Code, Sessions/Week, Course Type (Theory/Lab), Difficulty Level (High, Medium, Low), Faculty Member, Section.", "Course Constraints: ")
    add_bullet("Faculty Name, Faculty ID, Preferred Teaching Slots, Maximum Load, Assigned Courses.", "Faculty Constraints: ")
    add_bullet("Room Number, Room Capacity, Room Type (Classroom/Laboratory), Availability Status.", "Classroom Constraints: ")
    add_bullet("Section Name, Number of Students, Registered Courses.", "Student Section Constraints: ")
    add_bullet("Working Days (Monday to Friday), Available Time Periods, Academic Hours, Break Periods.", "Scheduling Constraints: ")

    add_p("Hard Constraints (Must always be satisfied):", bold_prefix="Enforced Hard Constraints: ")
    add_bullet("A faculty member cannot teach two classes at the same time.")
    add_bullet("A student section cannot attend two classes simultaneously.")
    add_bullet("A room cannot host multiple classes in the same time slot.")
    add_bullet("Laboratory courses must be scheduled only in laboratory rooms.")
    add_bullet("Room capacity must be sufficient for the enrolled students.")
    add_bullet("Each course must be allocated the required number of weekly sessions.")
    add_bullet("All scheduled sessions must occur within official academic hours.")

    add_h2("4.3 Output Constraints")
    add_p(
        "The output of the AI-Based University Timetable Generator is an optimized and validated weekly timetable "
        "that satisfies all hard constraints and attempts to optimize soft constraints. The generated timetable is "
        "displayed through the Streamlit dashboard in an organized format that is easy to understand and analyze."
    )
    add_bullet("Course Name, Faculty Name, Room Number, Student Section, Day of Allocation, Time Slot.", "Timetable Information: ")
    add_bullet("Zero Teacher Clashes, Zero Student Clashes, Zero Room Conflicts, Correct Lab Allocation, Room Capacity Compliance, Complete Session Allocation.", "Validation Output: ")
    add_bullet("Quality Score (0-100), Total Penalty Score, Faculty Preference Violations, Empty Period Count, Consecutive Difficult Subject Count, Course Distribution Penalty.", "Optimization Metrics: ")
    add_bullet("Weekly Timetable View, AI Analysis Dashboard, Algorithm Performance Comparison, Resource Utilization Statistics, Faculty Workload Analysis.", "Analytical Outputs: ")

    doc.add_page_break()

    # ==================== CHAPTER 5 ====================
    add_h1("Chapter 5: Hardware and Software Requirements")
    
    add_h2("5.1 Hardware Requirements")
    add_p(
        "The system can be executed on standard computer hardware without requiring specialized processing units. "
        "The minimum hardware configuration includes:"
    )
    add_bullet("Intel Core i3 / AMD equivalent", "Processor: ")
    add_bullet("4 GB", "RAM: ")
    add_bullet("1 GB free disk space", "Storage: ")
    add_bullet("1366 x 768 or higher", "Display Resolution: ")
    add_bullet("Recommended for GitHub integration and deployment", "Internet Connection: ")
    add_p("Recommended Configuration: Intel Core i5 or above, 8 GB RAM or higher, SSD Storage.", bold_prefix="Recommended: ")

    add_h2("5.2 Software Requirements")
    add_p("The software environment required for executing the project includes:")
    add_bullet("Windows 10/11, Linux, or macOS", "Operating System: ")
    add_bullet("Python 3.10+", "Programming Language: ")
    add_bullet("Streamlit", "Framework: ")
    add_bullet("Visual Studio Code, PyCharm, or Jupyter Notebook", "IDE: ")
    add_bullet("Git and GitHub", "Version Control: ")
    add_bullet("Streamlit, Pandas, NumPy, Matplotlib, Plotly, Pytest", "Libraries: ")

    doc.add_page_break()

    # ==================== CHAPTER 6 ====================
    add_h1("Chapter 6: Code Output and Design")
    
    add_h2("6.1 Code Quality and Modular Design")
    add_p(
        "The project follows a modular software architecture to ensure maintainability and scalability. "
        "Different functionalities such as CSP solving, constraint validation, timetable evaluation, "
        "optimization, visualization, and testing are implemented as separate modules. This promotes "
        "code reusability and simplifies debugging and future enhancements."
    )
    add_p(
        "Meaningful variable names, structured functions, extensive comments, and comprehensive documentation "
        "improve code readability. Dedicated test modules verify constraint handling, heuristic logic, CSP "
        "functionality, validation procedures, and timetable scoring mechanisms. The modular design "
        "significantly improves the robustness and reliability of the overall system."
    )

    add_h2("6.2 Program Execution and Results")
    add_p(
        "The application successfully generates conflict-free academic timetables through an interactive "
        "Streamlit interface. Users can generate optimized schedules by selecting scheduling parameters and "
        "initiating the CSP solver. Once generated, the timetable undergoes independent validation to confirm "
        "compliance with all hard constraints."
    )
    add_p(
        "The final schedule is presented in an organized weekly view showing course allocations, room "
        "assignments, faculty schedules, and section-specific timetables. Analysis dashboards provide detailed "
        "insights into timetable quality, performance metrics, and scheduling efficiency. Output screenshots "
        "demonstrating successful timetable generation and validation are included below:"
    )

    # Insert images if present
    img1 = "report_screenshots/01_initial_dashboard.png"
    if os.path.exists(img1):
        doc.add_picture(img1, width=Inches(6.0))
        p_cap = doc.add_paragraph("Figure 1.1: Starting Page & Initial Dashboard View")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)

    img2 = "report_screenshots/02_weekly_timetable.png"
    if os.path.exists(img2):
        doc.add_picture(img2, width=Inches(6.0))
        p_cap = doc.add_paragraph("Figure 1.2: Weekly University Timetable View (Section CSE-A)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)

    add_p("Figure 1.3: Timetable Generated Successfully with Zero Hard-Constraint Violations", italic=True)
    add_p("Figure 1.4: Timetable Generated for Section-B", italic=True)
    add_p("Figure 1.5: Detailed Schedule Breakdown (Subject, Faculty, Room, and Timing)", italic=True)
    add_p("Figure 1.6: AI Optimization Analysis Dashboard (Quality Score & Soft Penalties)", italic=True)
    add_p("Figure 1.7 & 1.8: Algorithm Comparison (Search Nodes Explored and Execution Runtime)", italic=True)

    add_h2("6.3 Performance Evaluation Metrics")
    add_p(
        "The quality of generated timetables is evaluated using multiple optimization metrics. These include: "
        "Empty Period Penalty, Consecutive Difficult Subject Penalty, Faculty Preference Violations, Course "
        "Distribution Penalty, and Overall Quality Score (0 to 100)."
    )

    add_h2("6.4 Working of the Algorithm and Observations")
    add_p(
        "The scheduling algorithm begins by representing each required course session as a CSP variable. "
        "Possible room-day-period combinations form the domain of each variable. The MRV heuristic identifies "
        "the most constrained variable, while the Degree Heuristic prioritizes highly connected scheduling decisions. "
        "Forward Checking removes invalid future assignments, thereby reducing the search space and improving efficiency."
    )
    add_p(
        "Experimental results indicate that the algorithm successfully generates valid timetables without teacher "
        "conflicts, room clashes, or section overlaps. The timetable scoring mechanism further improves schedule "
        "quality by minimizing undesirable arrangements and encouraging balanced academic planning. The "
        "observations confirm that CSP-based scheduling provides an efficient and scalable solution for "
        "university timetable management."
    )

    doc.add_page_break()

    # ==================== CHAPTER 7 ====================
    add_h1("Chapter 7: Time and Space Complexity")
    
    add_h2("7.1 Time Complexity Analysis")
    add_p(
        "Time Complexity analysis is used to estimate the amount of computational time required by the "
        "scheduling algorithm as the number of scheduling variables increases. Since the proposed timetable "
        "generator is based on a Constraint Satisfaction Problem (CSP), the complexity depends on the number "
        "of variables (course sessions) and the size of their domains (available room-day-period combinations)."
    )
    add_p(
        "In a basic CSP implementation using pure backtracking, the worst-case time complexity is:\n"
        "   O(d^n)\n"
        "where n = Number of variables (course sessions) and d = Number of possible assignments in domain."
    )
    add_p(
        "However, the proposed system improves efficiency using Minimum Remaining Values (MRV), Degree Heuristic, "
        "and Forward Checking. These optimization techniques significantly reduce the search space by selecting the "
        "most constrained variables first and eliminating invalid assignments before deeper exploration."
    )

    # Complexity Table
    tbl_comp = doc.add_table(rows=7, cols=2)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hdr = tbl_comp.rows[0].cells
    c_hdr[0].text = "Operation"
    c_hdr[1].text = "Complexity"
    for c in c_hdr:
        set_cell_background(c, "1B365D")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        c.paragraphs[0].runs[0].bold = True
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)

    comp_ops = [
        ("Variable Creation", "O(n)"),
        ("Domain Generation", "O(n * d)"),
        ("Constraint Validation", "O(n)"),
        ("MRV Variable Selection", "O(n)"),
        ("Forward Checking", "O(d)"),
        ("Backtracking Search", "O(d^n) Worst Case (exponentially pruned by MRV+FC)"),
    ]
    for i, (op, cval) in enumerate(comp_ops, start=1):
        row = tbl_comp.rows[i].cells
        row[0].text = op
        row[1].text = cval
        for c in row:
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            set_cell_background(c, "F9FAFB" if i % 2 == 1 else "FFFFFF")

    doc.add_paragraph()

    add_h2("7.2 Space Complexity Analysis")
    add_p(
        "Space Complexity represents the amount of memory required by the CSP algorithm during timetable generation. "
        "The system stores variables, domains, constraints, assignments, and recursive call stacks while searching "
        "for a solution."
    )
    add_p(
        "The overall space complexity can be approximated as:\n"
        "   O(n * d)\n"
        "where n is the number of scheduling variables and d is the number of domain values per variable. Additional "
        "memory is required for timetable validation, quality score evaluation, and analysis modules."
    )

    doc.add_page_break()

    # ==================== CHAPTER 8 ====================
    add_h1("Chapter 8: Features and Future Scope")
    
    add_h2("8.1 Key Features of the Project")
    add_p(
        "The AI-Based University Timetable Generator incorporates several advanced features that make it a practical "
        "and efficient scheduling solution for educational institutions. The system automatically generates "
        "conflict-free timetables by considering multiple scheduling constraints, thereby reducing manual effort and "
        "minimizing errors."
    )
    features = [
        "Automated University Timetable Generation",
        "Constraint Satisfaction Problem (CSP) Implementation",
        "Backtracking Search Algorithm with Forward Checking",
        "Minimum Remaining Values (MRV) and Degree Heuristics",
        "Hard Constraint Validation & Conflict Verification",
        "Soft Constraint Optimization & Quality Scoring",
        "Faculty Preference Management & Workload Balancing",
        "Laboratory vs. Classroom Smart Allocation",
        "Interactive Streamlit Web Dashboard",
        "Algorithm Comparison & Benchmarking View",
        "Modular Architecture with Pytest Automated Test Suite",
    ]
    for feat in features:
        add_bullet(feat)

    add_h2("8.2 Future Scope")
    add_p(
        "The proposed AI-Based University Timetable Generator provides a strong foundation for intelligent academic "
        "scheduling; however, several enhancements can be incorporated in future versions to further improve "
        "functionality, scalability, and user experience. The current implementation is designed using a modular "
        "architecture, making it suitable for integration with advanced technologies and institutional management "
        "systems."
    )

    add_h2("8.3 Future Enhancements")
    enhancements = [
        "Web-Based University Timetable Portal with Multi-User Authentication",
        "Cloud Deployment and Real-Time Institutional Database Integration",
        "Mobile Application Development for Students and Faculty",
        "Automatic Exam Timetable Generation and Attendance Integration",
        "Machine Learning-Based Faculty Preference & Attendance Prediction",
        "Genetic Algorithm & Hybrid Metaheuristic Optimization Models",
        "PDF, Excel, and Google Calendar Export Integrations",
    ]
    for enh in enhancements:
        add_bullet(enh)

    doc.add_page_break()

    # ==================== CHAPTER 9 ====================
    add_h1("Chapter 9: Innovation and Conclusion")
    
    add_h2("9.1 Innovation and Additional Features")
    add_p(
        "The project introduces several innovative features beyond basic timetable generation. The system performs "
        "timetable quality optimization, automated validation, faculty preference analysis, performance scoring, "
        "and algorithm comparison. The integration of Streamlit provides an interactive dashboard for visualization "
        "and analysis."
    )
    add_p(
        "Additional enhancements such as PDF export, Excel export, cloud deployment, machine learning-based "
        "recommendation systems, institutional database integration, and real-time timetable updates can be "
        "incorporated in future versions. These features increase the practical applicability and long-term "
        "value of the project."
    )

    add_h2("9.2 Conclusion")
    add_p(
        "The AI-Based University Timetable Generator demonstrates how Artificial Intelligence techniques can "
        "effectively solve complex academic scheduling problems. By utilizing CSP, Backtracking Search, MRV, "
        "Degree Heuristic, and Forward Checking, the system generates optimized and conflict-free timetables while "
        "maintaining high scheduling quality. The project reduces manual effort, improves resource utilization, "
        "and supports efficient academic planning. With its modular architecture, optimization capabilities, "
        "and user-friendly interface, the proposed system represents a practical and scalable solution for modern "
        "educational institutions."
    )

    doc.add_page_break()

    # ==================== CHAPTER 10 ====================
    add_h1("Chapter 10: References")
    refs = [
        "Python Tkinter documentation, Python Standard Library. https://docs.python.org/3/library/tk.html",
        "Python Official Documentation. https://docs.python.org",
        "Streamlit Documentation. https://docs.streamlit.io",
        "Russell, S., & Norvig, P. Artificial Intelligence: A Modern Approach. Pearson Education (CSP, MRV, Forward Checking).",
        "GitHub Repository: https://github.com/Utkarsh-Goswami857/Utkarsh-Goswami857",
    ]
    for ref in refs:
        add_bullet(ref)

    # Save to both file names
    out_path = "/Users/arizkhan0507/Downloads/AI_TimeTable_Generator/AI_University_Timetable_Generator_Project_Report.docx"
    doc.save(out_path)
    
    out_path2 = "/Users/arizkhan0507/Downloads/AI_TimeTable_Generator/PROJECT_REPORT.docx"
    doc.save(out_path2)
    print(f"Document successfully created:\n{out_path}\n{out_path2}")

if __name__ == "__main__":
    create_report_docx()
