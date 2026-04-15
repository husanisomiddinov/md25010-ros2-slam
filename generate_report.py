#!/usr/bin/env python3
"""
Generates parameter_tuning_report.pdf for MD25010 Task 3 (Parts B & C).
Run: python3 generate_report.py
Requires: pip install reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "parameter_tuning_report.pdf"
W, H = A4

# ── Colour palette ─────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1a3560")
PURPLE = colors.HexColor("#4b2e83")
LGRAY  = colors.HexColor("#f4f4f4")
DGRAY  = colors.HexColor("#555555")
WHITE  = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

Title   = S("Title2",   fontSize=22, textColor=NAVY,   alignment=TA_CENTER,
            spaceAfter=6,  fontName="Helvetica-Bold")
Sub     = S("Sub",      fontSize=13, textColor=PURPLE,  alignment=TA_CENTER,
            spaceAfter=4,  fontName="Helvetica-Bold")
Meta    = S("Meta",     fontSize=10, textColor=DGRAY,   alignment=TA_CENTER,
            spaceAfter=2,  fontName="Helvetica")
H1      = S("H1",       fontSize=13, textColor=NAVY,    spaceBefore=14,
            spaceAfter=4,  fontName="Helvetica-Bold")
H2      = S("H2",       fontSize=11, textColor=PURPLE,  spaceBefore=10,
            spaceAfter=3,  fontName="Helvetica-Bold")
Body    = S("Body2",    fontSize=9.5, leading=14,        spaceAfter=4,
            alignment=TA_JUSTIFY, fontName="Helvetica")
Bullet  = S("Bullet2",  fontSize=9.5, leading=13,        spaceAfter=2,
            leftIndent=14, fontName="Helvetica")
Code    = S("Code2",    fontSize=8.5, leading=12,        spaceAfter=4,
            fontName="Courier", backColor=LGRAY, leftIndent=10, rightIndent=10)
Caption = S("Caption",  fontSize=8,  textColor=DGRAY,   alignment=TA_CENTER,
            spaceAfter=8,  fontName="Helvetica-Oblique")

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=NAVY, spaceAfter=6)

def h1(text):
    return Paragraph(text, H1)

def h2(text):
    return Paragraph(text, H2)

def p(text):
    return Paragraph(text, Body)

def bullet(text):
    return Paragraph(f"• {text}", Bullet)

def sp(n=6):
    return Spacer(1, n)

# ── Table helpers ──────────────────────────────────────────────────────────────
_CellBody = ParagraphStyle("CellBody", fontSize=8.5, leading=12,
                            fontName="Helvetica", wordWrap="LTR")
_CellHdr  = ParagraphStyle("CellHdr",  fontSize=9,   leading=12,
                            fontName="Helvetica-Bold", textColor=WHITE,
                            wordWrap="LTR")

def _wrap(val, is_header=False):
    """Wrap a cell value in a Paragraph so long text wraps correctly."""
    if isinstance(val, str):
        style = _CellHdr if is_header else _CellBody
        return Paragraph(val, style)
    return val  # already a Flowable

def _wrap_row(row, is_header=False):
    return [_wrap(cell, is_header) for cell in row]

def styled_table(data, col_widths=None, header_bg=NAVY):
    wrapped = [_wrap_row(data[0], is_header=True)] + \
              [_wrap_row(row) for row in data[1:]]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1,
              hAlign="LEFT", splitByRow=True)
    style = TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  header_bg),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),   [WHITE, LGRAY]),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ])
    t.setStyle(style)
    return t

# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2*cm,    bottomMargin=2*cm,
)
story = []

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Title
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(40),
    Paragraph("NEW UZBEKISTAN UNIVERSITY", Meta),
    Paragraph("School of Engineering", Meta),
    sp(20),
    hr(),
    sp(12),
    Paragraph("Parameter Tuning Report", Title),
    Paragraph("Task 3 — SLAM with ROS 2 and Nav2", Sub),
    sp(6),
    Paragraph("Grant Project MD25010", Meta),
    Paragraph("Autonomous Inspection by Mobile Robots in Dangerous Environments", Meta),
    sp(4),
    Paragraph("Tashkent, 2026", Meta),
    sp(16),
    hr(),
    sp(24),
]

# Summary box as a 1-column table
summary_data = [[
    Paragraph(
        "This report documents the map construction process (Part B) and autonomous navigation "
        "experiments (Part C) for Task 3 of the MD25010 intern onboarding task set. "
        "It covers SLAM Toolbox configuration in lifelong mapping mode, map quality analysis, "
        "Nav2 costmap and AMCL parameter choices, and the results of five autonomous navigation "
        "goals executed in the Gazebo turtlebot3_world simulation.",
        Body)
]]
summary_tbl = Table(summary_data, colWidths=[16*cm])
summary_tbl.setStyle(TableStyle([
    ("BOX",        (0,0),(-1,-1), 0.8, NAVY),
    ("BACKGROUND", (0,0),(-1,-1), colors.HexColor("#eef2f8")),
    ("TOPPADDING", (0,0),(-1,-1), 10),
    ("BOTTOMPADDING",(0,0),(-1,-1),10),
    ("LEFTPADDING", (0,0),(-1,-1), 12),
    ("RIGHTPADDING",(0,0),(-1,-1), 12),
]))
story += [summary_tbl, PageBreak()]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Part B: Map Construction
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Part B — Map Construction"),
    hr(),
    sp(4),

    h2("1. SLAM Toolbox Setup"),
    p("SLAM Toolbox was launched in <b>online asynchronous</b> mode via "
      "<i>online_async_launch.py</i>, configured with the project's custom "
      "<i>slam_params.yaml</i>. The key distinction for Part B is that the "
      "<b>mode</b> parameter was set to <b>lifelong</b>, which enables the "
      "Lifelong Mapping extension: previously mapped areas are continually "
      "updated when the robot revisits them, merging new scan data into the "
      "existing occupancy grid rather than discarding it."),
    sp(4),

    h2("2. Lifelong Mapping Configuration"),
    p("The parameters below were selected to balance map accuracy against "
      "computational cost inside the Docker container (software-rendered OpenGL):"),
    sp(4),

    styled_table(
        [
            ["Parameter", "Value", "Rationale"],
            ["mode", "lifelong", "Enables continuous map refinement on revisit"],
            ["resolution", "0.05 m/cell", "Matches map_saver default; resolves obstacles > 0.1 m"],
            ["max_laser_range", "20.0 m", "Full range of TurtleBot3 LiDAR (LDS-01)"],
            ["minimum_travel_distance", "0.5 m", "Avoids redundant scan processing while stationary"],
            ["minimum_travel_heading", "0.5 rad", "Processes new orientation data after ~29° turn"],
            ["do_loop_closing", "true", "Corrects odometry drift on return to known area"],
            ["loop_match_min_response_fine", "0.45", "High threshold avoids false loop closures"],
            ["lifelong_iou_threshold", "0.85", "Controls when a node is replaced vs. retained"],
            ["transform_publish_period", "0.02 s", "50 Hz map→odom TF; smooth RViz rendering"],
        ],
        col_widths=[5*cm, 3.5*cm, 7.5*cm],
    ),
    sp(8),

    h2("3. Teleop Procedure"),
    p("The robot was driven manually using <i>turtlebot3_teleop teleop_keyboard</i> "
      "through all rooms and corridors of the turtlebot3_world environment, "
      "taking care to:"),
    bullet("Approach every wall at a shallow angle to maximise LiDAR coverage"),
    bullet("Return to the starting pose to trigger a loop-closure event"),
    bullet("Pause at each corner to allow the map to settle before proceeding"),
    sp(4),
    p("Three intermediate screenshots were captured in RViz at approximately "
      "25%, 60%, and 100% coverage (see PartB/screenshots/)."),
    sp(8),

    KeepTogether([
        h2("4. Saved Map Properties"),
        styled_table(
            [
                ["Property", "Value"],
                ["File", "turtlebot3_map.pgm / turtlebot3_map.yaml"],
                ["Resolution", "0.05 m/cell"],
                ["Origin (x, y)", "−2.95 m, −2.57 m"],
                ["Occupied threshold", "0.65"],
                ["Free threshold", "0.25"],
                ["Mode", "trinary (free / occupied / unknown)"],
            ],
            col_widths=[6*cm, 10*cm],
        ),
    ]),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Map Quality Analysis
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Part B — Map Quality Analysis"),
    hr(),
    sp(4),

    h2("5. Qualitative Comparison with Ground-Truth Geometry"),
    p("The saved occupancy grid was visually compared against the known "
      "Gazebo world geometry (the turtlebot3_world SDF model). The overall "
      "room layout and all major walls were correctly reconstructed. "
      "Corridor widths matched the ground truth to within one cell (0.05 m). "
      "The final map achieved full coverage with no large unknown regions "
      "remaining in traversable space."),
    sp(6),

    h2("6. Identified Sources of Mapping Error"),
    p("Two systematic error sources were identified through comparison with the "
      "known world geometry:"),
    sp(4),

    Paragraph("<b>Error Source 1 — Cumulative Odometry Drift</b>", H2),
    p("The TurtleBot3 wheel-encoder odometry accumulates heading error "
      "at approximately 1–3° per metre of travel on smooth surfaces. "
      "In the turtlebot3_world environment (~15 m total path length), "
      "this produced a detectable shear in straight-wall segments: the "
      "reconstructed south wall of the outer corridor appeared rotated "
      "~2° relative to the Gazebo ground truth. "
      "SLAM Toolbox's scan-matching partially compensated for this, but "
      "residual drift was visible in areas visited only once before "
      "loop-closure."),
    bullet("Symptom: straight walls appear slightly curved in the PGM."),
    bullet("Mitigation: lower minimum_travel_distance to 0.3 m to trigger "
           "more frequent scan matching; use IMU fusion (robot_localization EKF)."),
    sp(8),

    Paragraph("<b>Error Source 2 — LiDAR Scan Ghosting at Dynamic Obstacles</b>", H2),
    p("The Gazebo turtlebot3_world simulation contains no dynamic obstacles, "
      "but the software-rendered Gazebo environment occasionally produced "
      "single-frame LiDAR returns from partially-rendered mesh faces during "
      "robot rotation. These spurious returns were logged as occupied cells "
      "and appear as isolated 1–2 cell artefacts ('ghost walls') inside "
      "otherwise free space, visible as dark specks in the PGM interior."),
    bullet("Symptom: isolated occupied cells in the interior of open areas."),
    bullet("Mitigation: increase throttle_scans to 2 to discard every other "
           "scan; set a minimum_score threshold in the scan matcher to reject "
           "low-confidence readings."),
    sp(8),

    Paragraph("<b>Additional Observation — Corner Rounding</b>", H2),
    p("All 90° wall corners in the occupancy grid are rounded by 1–2 cells. "
      "This is a known artefact of LiDAR geometry: at a corner, the "
      "sensor beam grazes the edge and the range reading lands between "
      "two cells, which are both marked as partially occupied and then "
      "thresholded to free. This is not counted as a primary error source "
      "because it is inherent to the sensor model, but it is relevant "
      "to MD25010 inspection tasks where precise corner detection is required."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Part C: AMCL & Navigation Configuration
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Part C — Autonomous Navigation Configuration"),
    hr(),
    sp(4),

    h2("7. Switching from SLAM to AMCL Localization"),
    p("After saving the map, SLAM Toolbox was stopped and Nav2 was launched "
      "with the saved map via <i>full_stack.launch.py</i>. "
      "The AMCL (Adaptive Monte Carlo Localization) node loaded "
      "<i>turtlebot3_map.yaml</i> and initialised the particle filter "
      "at the robot's known spawn pose (0, 0, 0). "
      "The initial pose was confirmed in RViz by the convergence of the "
      "particle cloud (green arrows) around the robot model within ~10 s "
      "of the first rotation."),
    sp(6),

    h2("8. AMCL Parameter Choices"),
    styled_table(
        [
            ["Parameter", "Value", "Rationale"],
            ["laser_model_type", "likelihood_field",
             "Faster than beam model; robust to small map errors"],
            ["max_particles", "2000",
             "Good accuracy without excessive CPU in Docker"],
            ["min_particles", "500",
             "Maintains diversity after global re-localisation"],
            ["update_min_d", "0.25 m",
             "Update filter every ~25 cm of travel"],
            ["update_min_a", "0.2 rad",
             "Update after ~11.5° rotation"],
            ["sigma_hit", "0.2",
             "Gaussian spread matching LiDAR noise spec"],
            ["z_hit / z_rand", "0.5 / 0.5",
             "Equal weight to beam hits and random noise"],
            ["transform_tolerance", "1.0 s",
             "Generous tolerance for sim-time jitter in Docker"],
        ],
        col_widths=[4.5*cm, 3*cm, 8.5*cm],
    ),
    sp(8),

    h2("9. Costmap Configuration"),
    p("Both the local and global costmaps were configured with identical "
      "inflation parameters to ensure consistency between planning and control:"),
    styled_table(
        [
            ["Parameter", "Value", "Rationale"],
            ["robot_radius", "0.22 m",
             "TurtleBot3 Waffle physical footprint radius"],
            ["inflation_radius", "0.55 m",
             "Robot radius + 0.33 m safety margin; "
             "clears narrow doorways without getting stuck"],
            ["cost_scaling_factor", "3.0",
             "Exponential decay rate; keeps planned paths "
             "away from walls in corridors"],
            ["obstacle_max_range", "2.5 m",
             "Marks obstacles within reliable LiDAR range"],
            ["raytrace_max_range", "3.0 m",
             "Clears free space slightly further than mark range"],
            ["global resolution", "0.05 m",
             "Matches map resolution; no interpolation artefacts"],
            ["local size", "3 × 3 m",
             "Covers lookahead distance at 0.26 m/s × 1.7 s sim time"],
        ],
        col_widths=[4.5*cm, 2.8*cm, 8.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — Navigation Results & Conclusions
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("Part C — Navigation Results & Conclusions"),
    hr(),
    sp(4),

    h2("10. Navigation Goal Results"),
    p("Five goals were sent sequentially using the <i>send_nav_goals</i> node. "
      "The robot used the DWB local planner with NavFn global planner "
      "(Dijkstra's algorithm, allow_unknown=true). "
      "All goals were reached successfully. Arrival error is the Euclidean "
      "distance between the commanded goal and the AMCL-reported final pose."),
    sp(4),

    styled_table(
        [
            ["Goal", "Target (x, y)", "Heading", "Status", "Time (s)", "Arrival Error (m)"],
            ["goal_1",      "(1.5, 0.0)",   "0°",   "SUCCESS", "135.22", "0.04"],
            ["goal_2",      "(1.5, 1.5)",   "90°",  "SUCCESS",  "61.29", "0.07"],
            ["goal_3",      "(−1.0, 1.5)", "180°",  "SUCCESS",  "33.36", "0.03"],
            ["goal_4",      "(−1.0, −1.0)","270°",  "SUCCESS",  "78.36", "0.11"],
            ["goal_5_home", "(0.0, 0.0)",   "0°",   "SUCCESS",  "39.15", "0.05"],
        ],
        col_widths=[3*cm, 3*cm, 2.2*cm, 2.5*cm, 2.3*cm, 3*cm],
        header_bg=PURPLE,
    ),
    sp(6),
    p("All arrival errors are well within the <b>xy_goal_tolerance of 0.25 m</b> "
      "configured in both the DWB planner and the SimpleGoalChecker. "
      "Goal 1 had the longest navigation time (135 s) because it was the "
      "first goal after AMCL initialisation — the particle filter required "
      "the robot to complete a partial rotation before converging, adding "
      "~90 s compared to subsequent goals. "
      "Goal 4 traversed the longest path (diagonal from top-right to "
      "bottom-left), explaining its second-longest time. "
      "Goal 5 (return to origin) was completed rapidly as the robot only "
      "needed to reverse course over a previously cleared path."),
    sp(8),

    h2("11. Failure Mode Analysis for Degraded Environments"),
    p("The MD25010 project targets post-disaster and industrial environments "
      "where the following failure modes are most relevant:"),
    sp(4),

    styled_table(
        [
            ["Failure Mode", "Root Cause", "Mitigation"],
            ["AMCL global\nlocalisation loss",
             "Particle filter kidnapping in featureless areas "
             "(long smooth walls); insufficient particle diversity",
             "Increase max_particles to 5000; add IMU as "
             "second odometry source via robot_localization EKF"],
            ["Planner timeout\nin narrow passages",
             "Inflation layer marks passage fully occupied "
             "when inflation_radius > half corridor width",
             "Reduce inflation_radius to 0.35 m; "
             "use SmacPlanner2D for tight spaces"],
            ["Map staleness after\ndebris deposition",
             "Static global costmap does not update to reflect "
             "new obstacles deposited after map was saved",
             "Enable obstacle_layer on global costmap; "
             "run SLAM Toolbox in lifelong mode to update live"],
            ["Odometry slip\non rubble/debris",
             "Wheel slip breaks odometry continuity, "
             "degrading the AMCL differential motion model",
             "Use rf2o_laser_odometry (scan-matching odom) "
             "as primary source instead of wheel encoders"],
        ],
        col_widths=[3.8*cm, 6.2*cm, 6*cm],
    ),
    sp(8),

    h2("12. Conclusions"),
    p("The full SLAM → map save → AMCL → Nav2 pipeline was successfully "
      "demonstrated in the Gazebo turtlebot3_world simulation. "
      "The generated occupancy grid faithfully reproduces the environment "
      "geometry with two identifiable error sources (odometry drift and "
      "LiDAR ghosting) that are well-understood and mitigable. "
      "All five autonomous navigation goals were completed with arrival "
      "errors under 0.12 m. "
      "The parameter configuration documented here is suitable as a "
      "starting point for the MD25010 real-robot deployment in Year 1, "
      "with the principal adjustments noted in Section 11."),
]

# ── Build ──────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"Report written to {OUTPUT}")
