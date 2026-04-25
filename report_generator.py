"""
pdf_generator.py  –  Polished PDF report for AI Resume Analyzer
"""
import os, tempfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

OLIVE=colors.HexColor("#3D6B35"); OLIVE_LT=colors.HexColor("#D8EDD4")
BLUE=colors.HexColor("#2556A0");  BLUE_LT=colors.HexColor("#D3E2F5")
RUST=colors.HexColor("#9E3A2B");  RUST_LT=colors.HexColor("#F4DAD6")
GOLD=colors.HexColor("#8A5C0A");  GOLD_LT=colors.HexColor("#F5E8CA")
BG=colors.HexColor("#F5F3EE");    SURFACE=colors.HexColor("#FEFDFB")
BORDER=colors.HexColor("#E2DED5");INK=colors.HexColor("#1A1916")
INK2=colors.HexColor("#64625C");  INK3=colors.HexColor("#A09D96")
PAGE_W,PAGE_H=A4; MARGIN=18*mm

def safe_str(item)->str:
    if item is None: return ""
    if isinstance(item,str): return item.strip()
    if isinstance(item,(int,float)): return str(item)
    if isinstance(item,dict):
        for k in("title","text","name","label","value","description"):
            if k in item and item[k]:
                v=str(item[k]).strip()
                return f"{v} ({item['link']})" if item.get("link") else v
        parts=[str(v) for v in item.values() if v and isinstance(v,(str,int,float))]
        return " – ".join(parts) if parts else str(item)
    if isinstance(item,(list,tuple)): return ", ".join(safe_str(x) for x in item)
    return str(item).strip()

def safe_list(lst)->list:
    if not lst or not isinstance(lst,list): return []
    return [s for s in(safe_str(x) for x in lst) if s]

def _fig_score_bars(ats,ai,path):
    fig,ax=plt.subplots(figsize=(6.2,2.2),facecolor="#F5F3EE")
    ax.set_facecolor("#F5F3EE")
    bars=ax.barh(["ATS Score","AI Score"],[ats,ai],color=["#3D6B35","#2556A0"],height=0.45,edgecolor="none")
    for bar,val in zip(bars,[ats,ai]):
        ax.text(val+1.2,bar.get_y()+bar.get_height()/2,f"{val}%",va="center",ha="left",fontsize=11,fontweight="bold",color="#1A1916")
    ax.set_xlim(0,115); ax.set_xlabel("Score (%)",fontsize=9,color="#64625C")
    ax.tick_params(colors="#64625C",labelsize=10)
    for sp in["top","right"]: ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#E2DED5"); ax.spines["bottom"].set_color("#E2DED5")
    ax.set_axisbelow(True); ax.xaxis.grid(True,color="#E2DED5",linewidth=0.8)
    fig.tight_layout(pad=0.5); fig.savefig(path,dpi=150,bbox_inches="tight",facecolor="#F5F3EE"); plt.close(fig)
    return path

def _fig_donut(ats,path):
    fig,ax=plt.subplots(figsize=(3,3),facecolor="#F5F3EE")
    ax.set_facecolor("#F5F3EE")
    ax.pie([ats,max(0,100-ats)],colors=["#3D6B35","#E2DED5"],startangle=90,
           wedgeprops=dict(width=0.42,edgecolor="#F5F3EE",linewidth=2),counterclock=False)
    ax.text(0,0.08,f"{ats}%",ha="center",va="center",fontsize=22,fontweight="bold",color="#1A1916")
    ax.text(0,-0.25,"ATS Score",ha="center",va="center",fontsize=9,color="#64625C")
    fig.tight_layout(pad=0); fig.savefig(path,dpi=150,bbox_inches="tight",facecolor="#F5F3EE"); plt.close(fig)
    return path

def _fig_skills(skills,path):
    n=min(len(skills),12)
    if n==0: return None
    fig,ax=plt.subplots(figsize=(5.5,max(2.2,n*0.38)),facecolor="#F5F3EE")
    ax.set_facecolor("#F5F3EE"); y=range(n)
    ax.hlines(y,0,100,colors="#D8EDD4",linewidth=4,zorder=1)
    ax.scatter([100]*n,y,color="#3D6B35",s=60,zorder=2)
    ax.set_yticks(list(y)); ax.set_yticklabels(skills[:n],fontsize=9,color="#1A1916")
    ax.set_xlim(0,120); ax.set_xticks([])
    for sp in["top","right","bottom"]: ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#E2DED5"); ax.tick_params(left=False)
    fig.tight_layout(pad=0.4); fig.savefig(path,dpi=150,bbox_inches="tight",facecolor="#F5F3EE"); plt.close(fig)
    return path

def _styles():
    base=getSampleStyleSheet()
    def ps(n,**kw):
        p=kw.pop("parent",base["Normal"]); return ParagraphStyle(n,parent=p,**kw)
    return{
        "title":   ps("T",fontName="Helvetica-Bold",fontSize=22,textColor=INK,alignment=TA_LEFT,spaceAfter=2),
        "subtitle":ps("S",fontName="Helvetica",fontSize=10,textColor=INK2,alignment=TA_LEFT,spaceAfter=0),
        "section": ps("SE",fontName="Helvetica-Bold",fontSize=12,textColor=OLIVE,spaceBefore=6,spaceAfter=4),
        "body":    ps("B",fontName="Helvetica",fontSize=9.5,textColor=INK2,leading=15,spaceAfter=3),
        "explain": ps("EX",fontName="Helvetica",fontSize=9.5,textColor=colors.HexColor("#1C3E78"),
                      backColor=BLUE_LT,leading=15,leftIndent=8,rightIndent=8,borderPadding=(6,8,6,8)),
        "grade_A": ps("GA",fontName="Helvetica-Bold",fontSize=10,textColor=OLIVE,backColor=OLIVE_LT,
                      alignment=TA_CENTER,borderPadding=(4,10,4,10)),
        "grade_B": ps("GB",fontName="Helvetica-Bold",fontSize=10,textColor=GOLD,backColor=GOLD_LT,
                      alignment=TA_CENTER,borderPadding=(4,10,4,10)),
        "grade_C": ps("GC",fontName="Helvetica-Bold",fontSize=10,textColor=RUST,backColor=RUST_LT,
                      alignment=TA_CENTER,borderPadding=(4,10,4,10)),
        "footer":  ps("F",fontName="Helvetica",fontSize=7.5,textColor=INK3,alignment=TA_CENTER),
        "caption": ps("C",fontName="Helvetica",fontSize=8,textColor=INK3,alignment=TA_CENTER,spaceAfter=6),
    }

def _on_first_page(canvas,doc): _hdr(canvas); _ftr(canvas,doc)
def _on_later_pages(canvas,doc): _hdr(canvas); _ftr(canvas,doc)
def _hdr(canvas):
    canvas.saveState()
    canvas.setFillColor(OLIVE); canvas.rect(0,PAGE_H-10*mm,PAGE_W,10*mm,fill=1,stroke=0)
    canvas.setFillColor(OLIVE_LT); canvas.circle(PAGE_W-22*mm,PAGE_H-5*mm,3*mm,fill=1,stroke=0)
    canvas.restoreState()
def _ftr(canvas,doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,PAGE_W,12*mm,fill=1,stroke=0)
    canvas.setFillColor(BORDER); canvas.rect(0,12*mm,PAGE_W,0.3*mm,fill=1,stroke=0)
    canvas.setFont("Helvetica",7.5); canvas.setFillColor(INK3)
    canvas.drawString(MARGIN,4.5*mm,"AI Resume Analyzer  •  Confidential Report")
    canvas.drawRightString(PAGE_W-MARGIN,4.5*mm,f"Page {doc.page}")
    canvas.restoreState()

def _sec(title,S):
    return[Spacer(1,6*mm),HRFlowable(width="100%",thickness=0.5,color=BORDER,spaceAfter=4),
           Paragraph(title.upper(),S["section"]),Spacer(1,2*mm)]

def _pills(items,pill_color,bg,bdr,cols=4):
    if not items: return[]
    cells=[]
    for item in items:
        t=safe_str(item)
        if not t: continue
        cells.append(Table([[Paragraph(t,ParagraphStyle("pi",fontName="Helvetica-Bold",fontSize=8.5,textColor=pill_color))]],
            colWidths=[None],style=TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("ROUNDEDCORNERS",[4]),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),("BOX",(0,0),(-1,-1),0.5,bdr)])))
    if not cells: return[]
    while len(cells)%cols: cells.append(Paragraph("",ParagraphStyle("pe")))
    rows=[cells[i:i+cols] for i in range(0,len(cells),cols)]
    cw=(PAGE_W-2*MARGIN)/cols
    return[Table(rows,colWidths=[cw]*cols,style=TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
           ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
           ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3)])),Spacer(1,3*mm)]

def _score_tbl(ats,ai,grade,S):
    gl={"A":"Grade A — Strong Pass","B":"Grade B — Moderate Pass","C":"Grade C — Needs Work"}
    cw=(PAGE_W-2*MARGIN)/3
    d=[[Paragraph(f"<b>{ats}%</b>",ParagraphStyle("sa",fontName="Helvetica-Bold",fontSize=22,textColor=OLIVE,alignment=TA_CENTER)),
        Paragraph(f"<b>{ai}%</b>", ParagraphStyle("sb",fontName="Helvetica-Bold",fontSize=22,textColor=BLUE, alignment=TA_CENTER)),
        Paragraph(gl[grade],S[f"grade_{grade}"])],
       [Paragraph("ATS Rule Score",ParagraphStyle("sl1",fontName="Helvetica",fontSize=8,textColor=INK3,alignment=TA_CENTER)),
        Paragraph("AI Score",      ParagraphStyle("sl2",fontName="Helvetica",fontSize=8,textColor=INK3,alignment=TA_CENTER)),
        Paragraph("",S["body"])]]
    return Table(d,colWidths=[cw,cw,cw],style=TableStyle([
        ("BACKGROUND",(0,0),(0,-1),OLIVE_LT),("BACKGROUND",(1,0),(1,-1),BLUE_LT),("BACKGROUND",(2,0),(2,-1),GOLD_LT),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("BOX",(0,0),(0,-1),0.5,colors.HexColor("#B4D9AE")),
        ("BOX",(1,0),(1,-1),0.5,colors.HexColor("#BAD0EE")),
        ("BOX",(2,0),(2,-1),0.5,colors.HexColor("#DEC07E")),("ROUNDEDCORNERS",[6])]))

def generate_pdf(data:dict,filename:str="resume_report.pdf")->str:
    S=_styles(); tmp=tempfile.gettempdir()

    # ✅ Sanitize everything from backend
    ats        = int(data["analysis"].get("score",0))
    ai         = int(data.get("ai_analysis",{}).get("score",0))
    explanation= safe_str(data["analysis"].get("explanation",""))
    skills     = safe_list(data.get("skills",[]))
    missing    = safe_list(data["analysis"].get("missing_skills",[]))
    sug_rule   = safe_list(data["analysis"].get("suggestions",[]))
    ai_missing = safe_list(data.get("ai_analysis",{}).get("missing_skills",[]))
    sug_ai     = safe_list(data.get("ai_analysis",{}).get("suggestions",[]))
    all_miss   = missing+[s for s in ai_missing if s not in missing]
    all_sug    = sug_ai +[s for s in sug_rule   if s not in sug_ai]
    grade      = "A" if ats>=80 else "B" if ats>=60 else "C"

    bp=os.path.join(tmp,"ra_bars.png"); dp=os.path.join(tmp,"ra_donut.png"); sp=os.path.join(tmp,"ra_skills.png")
    _fig_score_bars(ats,ai,bp); _fig_donut(ats,dp); sc=_fig_skills(skills,sp)

    doc=SimpleDocTemplate(filename,pagesize=A4,topMargin=16*mm,bottomMargin=18*mm,leftMargin=MARGIN,rightMargin=MARGIN)
    E=[]; cw=PAGE_W-2*MARGIN

    E+=[Spacer(1,4*mm),Paragraph("AI Resume Analysis Report",S["title"]),
        Paragraph("Automated ATS scoring, skill gap detection &amp; improvement suggestions",S["subtitle"]),
        Spacer(1,5*mm),HRFlowable(width="100%",thickness=1.5,color=OLIVE,spaceAfter=6)]

    E+=_sec("Score Overview",S)+[_score_tbl(ats,ai,grade,S),Spacer(1,5*mm)]

    E.append(Table([[Image(bp,width=cw*0.62,height=60*mm),Image(dp,width=cw*0.34,height=60*mm)]],
        colWidths=[cw*0.64,cw*0.36],style=TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("BACKGROUND",(0,0),(-1,-1),SURFACE),
        ("BOX",(0,0),(-1,-1),0.5,BORDER),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)])))

    if explanation:
        E+=_sec("Score Explanation",S)+[Paragraph(explanation,S["explain"])]

    E+=_sec(f"Skills Found  ({len(skills)})",S)
    if skills:
        E+=_pills(skills,OLIVE,OLIVE_LT,colors.HexColor("#B4D9AE"))
        if sc:
            E+=[Image(sc,width=cw*0.7,height=max(30*mm,len(skills[:12])*10)),
                Paragraph("Skills presence chart",S["caption"])]
    else:
        E+=[Paragraph("No skills detected.",S["body"])]

    E+=_sec(f"Missing Skills  ({len(all_miss)})",S)
    E+=_pills(all_miss,RUST,RUST_LT,colors.HexColor("#EDBBB4")) if all_miss else[Paragraph("No missing skills — great coverage!",S["body"])]

    E+=_sec(f"Improvement Suggestions  ({len(all_sug)})",S)
    if all_sug:
        for i,sug in enumerate(all_sug,1):
            E.append(Table([[
                Paragraph(f"<b>{i}</b>",ParagraphStyle("sn",fontName="Helvetica-Bold",fontSize=9,textColor=GOLD,alignment=TA_CENTER)),
                Paragraph(safe_str(sug),S["body"])   # ✅ safe_str again as extra guard
            ]],colWidths=[8*mm,cw-8*mm],style=TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                ("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2),
                ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0)])))
            if i<len(all_sug):
                E.append(HRFlowable(width="100%",thickness=0.3,color=BORDER,spaceAfter=2,spaceBefore=2))
    else:
        E+=[Paragraph("No suggestions — your resume looks excellent!",S["body"])]

    E+=[Spacer(1,8*mm),HRFlowable(width="100%",thickness=0.5,color=BORDER),Spacer(1,3*mm),
        Paragraph("This report was generated automatically by the AI Resume Analyzer. "
                  "Scores are indicative and should be used as guidance alongside human review.",S["footer"])]

    doc.build(E,onFirstPage=_on_first_page,onLaterPages=_on_later_pages)
    for p in[bp,dp,sp]:
        try: os.remove(p)
        except FileNotFoundError: pass
    return filename

if __name__=="__main__":
    SAMPLE={"skills":["Python","Java","Spring Boot","MySQL","REST APIs","React","Node.js","Git","Scikit-learn","OpenCV","Pandas","NumPy"],
        "analysis":{"score":76,"explanation":"Strong backend & ML coverage. DevOps keywords missing.",
            "missing_skills":[{"title":"Docker","link":"https://docker.com"},{"title":"Kubernetes","link":""},"AWS","CI/CD"],
            "suggestions":[{"title":"Add quantified impact.","link":""},"Include deployed project links."]},
        "ai_analysis":{"score":71,"missing_skills":[{"title":"Terraform"},"GraphQL"],
            "suggestions":["Tailor summary per application.",{"title":"Vary action verbs.","link":None}]}}
    print(f"✅ PDF saved → {generate_pdf(SAMPLE,'sample_report.pdf')}")