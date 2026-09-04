from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>NCC Attendance Report</title>

<style>
*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

body{
    font-family:Arial, sans-serif;
    min-height:100vh;
    background:
        radial-gradient(circle at top left,#17233d,transparent 40%),
        radial-gradient(circle at bottom right,#182b20,transparent 40%),
        #080b12;
    color:white;
    padding:25px 0 50px;
}

.container{
    width:min(1250px,96%);
    margin:auto;
}

.tabs{
    display:flex;
    gap:15px;
    margin-bottom:25px;
}

.tab{
    flex:1;
    border:none;
    border-radius:18px;
    min-height:62px;
    font-size:20px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:#151b28;
    border:1px solid rgba(255,255,255,.12);
    transition:.25s;
}

.tab.active{
    background:linear-gradient(135deg,#246bfd,#7048ff);
    box-shadow:0 10px 30px rgba(70,90,255,.3);
}

.card{
    background:rgba(18,23,34,.92);
    border:1px solid rgba(255,255,255,.1);
    border-radius:25px;
    padding:32px;
    margin-bottom:25px;
    box-shadow:0 15px 50px rgba(0,0,0,.25);
}

.title{
    font-size:28px;
    font-weight:800;
    margin-bottom:22px;
}

.inputs{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:18px;
    margin-bottom:20px;
}

input,textarea{
    width:100%;
    background:#0d121c;
    color:white;
    border:1px solid #30394c;
    border-radius:14px;
    outline:none;
    font-size:18px;
    padding:16px;
}

input{
    min-height:58px;
}

textarea{
    min-height:180px;
    resize:vertical;
}

input:focus,textarea:focus{
    border-color:#5585ff;
    box-shadow:0 0 0 3px rgba(85,133,255,.12);
}

.controls{
    display:flex;
    flex-wrap:wrap;
    gap:12px;
    margin-top:15px;
}

.btn{
    border:none;
    border-radius:13px;
    padding:14px 20px;
    min-height:52px;
    color:white;
    font-size:16px;
    font-weight:bold;
    cursor:pointer;
    background:#202a3c;
    border:1px solid rgba(255,255,255,.1);
    transition:.2s;
}

.btn:hover{
    transform:translateY(-2px);
}

.save{
    background:#16794d;
}

.load{
    background:#2858b8;
}

.clear{
    background:#8b2933;
}

.summary{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
    margin-top:20px;
}

.summary-box{
    min-height:100px;
    padding:18px;
    border-radius:18px;
    background:#111827;
    border:1px solid rgba(255,255,255,.08);
    text-align:center;
}

.summary-number{
    font-size:32px;
    font-weight:900;
    margin-top:8px;
}

.present-box .summary-number{
    color:#35d47a;
}

.absent-box .summary-number{
    color:#ff5362;
}

.permission-box .summary-number{
    color:#ffd84d;
}

.late-box .summary-number{
    color:#ff9b32;
}

.attendance{
    position:relative;
    overflow:hidden;
    min-height:180px;
    margin-top:25px;
    padding:38px;
    border-radius:22px;
    background:#0c111a;
    border:1px solid rgba(255,255,255,.08);
}

.cadet-list{
    position:relative;
    z-index:2;
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:13px;
}

.cadet{
    position:relative;
    overflow:hidden;
    width:max-content;
    max-width:95%;
    min-width:190px;
    min-height:55px;
    padding:15px 30px;
    border-radius:15px;
    border:2px solid transparent;
    color:white;
    font-size:17px;
    font-weight:800;
    cursor:pointer;
    transition:.2s;
    box-shadow:0 7px 20px rgba(0,0,0,.25);
}

.cadet:hover{
    transform:scale(1.03);
}

.cadet::before{
    content:"";
    position:absolute;
    top:0;
    left:-120%;
    width:80%;
    height:100%;
    transform:skewX(-25deg);
    background:linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,.35),
        transparent
    );
    animation:shine 3.5s infinite;
}

.cadet::after{
    content:"✦";
    position:absolute;
    right:10px;
    top:5px;
    font-size:11px;
    animation:sparkle 1.8s infinite;
}

@keyframes shine{
    0%{left:-120%}
    55%,100%{left:140%}
}

@keyframes sparkle{
    0%,100%{
        opacity:.2;
        transform:scale(.7);
    }
    50%{
        opacity:1;
        transform:scale(1.2);
    }
}

.status-absent{
    background:#a62935;
    border-color:#ff5362;
}

.status-present{
    background:#137445;
    border-color:#35d47a;
}

.status-permission{
    background:#b28a08;
    border-color:#ffd84d;
}

.status-late{
    background:#b75d13;
    border-color:#ff9b32;
}

.generate{
    width:100%;
    margin-top:25px;
    min-height:65px;
    border:none;
    border-radius:17px;
    background:linear-gradient(135deg,#246bfd,#7048ff);
    color:white;
    font-size:20px;
    font-weight:900;
    cursor:pointer;
    box-shadow:0 12px 30px rgba(50,90,255,.3);
}

.report-card{
    display:none;
    margin-top:25px;
    padding:25px;
    border-radius:20px;
    background:#0b1019;
    border:1px solid #29344a;
}

.report-title{
    font-size:21px;
    font-weight:800;
    margin-bottom:15px;
}

.report{
    white-space:pre-wrap;
    line-height:1.65;
    font-size:16px;
    background:#080c13;
    border-radius:14px;
    padding:20px;
    user-select:text;
}

.copy{
    margin-top:15px;
    background:#1667b1;
}

.page{
    display:none;
}

.page.active{
    display:block;
}

.empty{
    text-align:center;
    color:#8791a4;
    padding:30px;
}

@media(max-width:650px){

    body{
        padding:12px 0 30px;
    }

    .container{
        width:94%;
    }

    .tabs{
        gap:8px;
    }

    .tab{
        min-height:52px;
        font-size:15px;
        border-radius:14px;
    }

    .card{
        padding:18px;
        border-radius:20px;
    }

    .title{
        font-size:23px;
    }

    .inputs{
        grid-template-columns:1fr;
    }

    input,textarea{
        font-size:16px;
    }

    .summary{
        grid-template-columns:1fr 1fr;
        gap:10px;
    }

    .summary-box{
        min-height:85px;
        padding:13px;
    }

    .summary-number{
        font-size:26px;
    }

    .attendance{
        padding:25px 12px;
    }

    .cadet{
        min-width:160px;
        font-size:15px;
        padding:14px 22px;
    }

    .controls .btn{
        flex:1 1 45%;
    }

    .generate{
        font-size:18px;
    }
}
</style>
</head>

<body>

<div class="container">

<div class="tabs">
    <button class="tab active"
            id="tabSecond"
            onclick="switchPage('second')">
        2nd Year SD
    </button>

    <button class="tab"
            id="tabFirst"
            onclick="switchPage('first')">
        1st Year SD
    </button>
</div>


<!-- SECOND YEAR -->

<div id="pageSecond" class="page active">

<div class="card">

<div class="title">
    2nd Year SD Attendance
</div>

<div class="inputs">

<input
    id="year2"
    type="text"
    placeholder="Year">

<input
    id="strength2"
    type="text"
    placeholder="Total Strength">

</div>

<textarea
    id="names2"
    placeholder="Enter CDT names one per line"></textarea>


<div class="controls">

<button class="btn save"
        onclick="saveNames('second')">
    Save Names
</button>

<button class="btn load"
        onclick="loadNames('second')">
    Load Names
</button>

<button class="btn clear"
        onclick="clearNames('second')">
    Clear Saved Names
</button>

</div>


<div class="summary">

<div class="summary-box present-box">
    <div>Present</div>
    <div class="summary-number" id="present2">0</div>
</div>

<div class="summary-box absent-box">
    <div>Absent</div>
    <div class="summary-number" id="absent2">0</div>
</div>

<div class="summary-box permission-box">
    <div>Permission</div>
    <div class="summary-number" id="permission2">0</div>
</div>

<div class="summary-box late-box">
    <div>Late Fall-in</div>
    <div class="summary-number" id="late2">0</div>
</div>

</div>


<div class="attendance">

<div id="cadets2" class="cadet-list">

<div class="empty">
    Save or load CDT names to begin.
</div>

</div>

</div>


<button class="generate"
        onclick="generateReport('second')">
    Generate Report
</button>


<div id="reportCard2" class="report-card">

<div class="report-title">
    Reporting Seniors
</div>

<div id="report2" class="report"></div>

<button class="btn copy"
        onclick="copyReport('second',this)">
    Copy Report
</button>

</div>

</div>
</div>



<!-- FIRST YEAR -->

<div id="pageFirst" class="page">

<div class="card">

<div class="title">
    1st Year SD Attendance
</div>

<div class="inputs">

<input
    id="year1"
    type="text"
    placeholder="Year">

<input
    id="strength1"
    type="text"
    placeholder="Total Strength">

</div>

<textarea
    id="names1"
    placeholder="Enter CDT names one per line"></textarea>


<div class="controls">

<button class="btn save"
        onclick="saveNames('first')">
    Save Names
</button>

<button class="btn load"
        onclick="loadNames('first')">
    Load Names
</button>

<button class="btn clear"
        onclick="clearNames('first')">
    Clear Saved Names
</button>

</div>


<div class="summary">

<div class="summary-box present-box">
    <div>Present</div>
    <div class="summary-number" id="present1">0</div>
</div>

<div class="summary-box absent-box">
    <div>Absent</div>
    <div class="summary-number" id="absent1">0</div>
</div>

<div class="summary-box permission-box">
    <div>Permission</div>
    <div class="summary-number" id="permission1">0</div>
</div>

<div class="summary-box late-box">
    <div>Late Fall-in</div>
    <div class="summary-number" id="late1">0</div>
</div>

</div>


<div class="attendance">

<div id="cadets1" class="cadet-list">

<div class="empty">
    Save or load CDT names to begin.
</div>

</div>

</div>


<button class="generate"
        onclick="generateReport('first')">
    Generate Report
</button>


<div id="reportCard1" class="report-card">

<div class="report-title">
    Reporting Seniors
</div>

<div id="report1" class="report"></div>

<button class="btn copy"
        onclick="copyReport('first',this)">
    Copy Report
</button>

</div>

</div>
</div>

</div>


<script>

const STORAGE = {
    second:"ncc_2nd_year_names_v5",
    first:"ncc_1st_year_names_v5"
};


let data = {
    second:{
        cadets:[]
    },

    first:{
        cadets:[]
    }
};



function switchPage(page){

    document
        .getElementById("pageSecond")
        .classList.toggle(
            "active",
            page === "second"
        );

    document
        .getElementById("pageFirst")
        .classList.toggle(
            "active",
            page === "first"
        );

    document
        .getElementById("tabSecond")
        .classList.toggle(
            "active",
            page === "second"
        );

    document
        .getElementById("tabFirst")
        .classList.toggle(
            "active",
            page === "first"
        );
}



function saveNames(page){

    const suffix =
        page === "second" ? "2" : "1";

    const names =
        document
        .getElementById("names"+suffix)
        .value
        .split("\n")
        .map(name => name.trim())
        .filter(Boolean);

    if(names.length === 0){

        alert("Please enter CDT names first.");

        return;
    }


    localStorage.setItem(
        STORAGE[page],
        JSON.stringify(names)
    );


    data[page].cadets =
        names.map(name => ({
            name:name,
            taps:0,
            status:"Absent"
        }));


    render(page);

    alert("✅ Names saved successfully!");
}



function loadNames(page){

    const suffix =
        page === "second" ? "2" : "1";

    const saved =
        localStorage.getItem(
            STORAGE[page]
        );


    if(!saved){

        alert("No saved names found.");

        return;
    }


    const names =
        JSON.parse(saved);


    document
        .getElementById("names"+suffix)
        .value =
        names.join("\n");


    data[page].cadets =
        names.map(name => ({
            name:name,
            taps:0,
            status:"Absent"
        }));


    render(page);
}



function clearNames(page){

    if(!confirm(
        "Clear saved names?"
    )) return;


    localStorage.removeItem(
        STORAGE[page]
    );


    const suffix =
        page === "second" ? "2" : "1";


    document
        .getElementById("names"+suffix)
        .value = "";


    data[page].cadets = [];


    render(page);
}



function cycle(page,index){

    const states = [
        "Absent",
        "Present",
        "Permission",
        "Late Fall-in Permission"
    ];


    const cadet =
        data[page].cadets[index];


    cadet.taps =
        (cadet.taps + 1) % 4;


    cadet.status =
        states[cadet.taps];


    render(page);
}



function render(page){

    const suffix =
        page === "second" ? "2" : "1";


    const container =
        document.getElementById(
            "cadets"+suffix
        );


    container.innerHTML = "";


    if(data[page].cadets.length === 0){

        container.innerHTML =
            '<div class="empty">Save or load CDT names to begin.</div>';

        updateSummary(page);

        return;
    }


    data[page].cadets.forEach(
        (cadet,index) => {

            const button =
                document.createElement("button");


            button.className =
                "cadet " +
                statusClass(cadet.status);


            button.textContent =
                cadet.name;


            button.title =
                cadet.status;


            button.onclick =
                () => cycle(page,index);


            container.appendChild(button);
        }
    );


    updateSummary(page);
}



function statusClass(status){

    if(status === "Present")
        return "status-present";

    if(status === "Permission")
        return "status-permission";

    if(status === "Late Fall-in Permission")
        return "status-late";

    return "status-absent";
}



function updateSummary(page){

    const suffix =
        page === "second" ? "2" : "1";


    const cadets =
        data[page].cadets;


    const present =
        cadets.filter(
            c => c.status === "Present"
        ).length;


    const absent =
        cadets.filter(
            c => c.status === "Absent"
        ).length;


    const permission =
        cadets.filter(
            c => c.status === "Permission"
        ).length;


    const late =
        cadets.filter(
            c => c.status === "Late Fall-in Permission"
        ).length;


    document.getElementById(
        "present"+suffix
    ).textContent = present;


    document.getElementById(
        "absent"+suffix
    ).textContent = absent;


    document.getElementById(
        "permission"+suffix
    ).textContent = permission;


    document.getElementById(
        "late"+suffix
    ).textContent = late;
}



function generateReport(page){

    const suffix =
        page === "second" ? "2" : "1";


    const year =
        document
        .getElementById("year"+suffix)
        .value
        .trim();


    const strength =
        document
        .getElementById("strength"+suffix)
        .value
        .trim();


    const cadets =
        data[page].cadets;


    if(cadets.length === 0){

        alert(
            "Please load CDT names first."
        );

        return;
    }


    const present =
        cadets.filter(
            c => c.status === "Present"
        );


    const permission =
        cadets.filter(
            c => c.status === "Permission"
        );


    const late =
        cadets.filter(
            c => c.status === "Late Fall-in Permission"
        );


    const absent =
        cadets.filter(
            c => c.status === "Absent"
        );


    let text =
`REPORTING SENIORS,

${year} total strength ${strength} seniors,

`;


    if(present.length > 0){

        text +=
`At present ${present.length} seniors,

${present.map(c => c.name).join("\n")}

`;
    }


    if(permission.length > 0){

        text +=
`${permission.length} permission seniors,

${permission.map(c => c.name).join("\n")}

`;
    }


    if(late.length > 0){

        text +=
`${String(late.length).padStart(2,"0")} late fallin permission seniors,

${late.map(c => c.name).join("\n")}

`;
    }


    if(absent.length > 0){

        text +=
`${absent.length} absent seniors,

${absent.map(c => c.name).join("\n")}`;
    }


    const report =
        text.trim();


    document.getElementById(
        "report"+suffix
    ).textContent =
        report;


    document.getElementById(
        "reportCard"+suffix
    ).style.display =
        "block";
}



async function copyReport(page,button){

    const suffix =
        page === "second" ? "2" : "1";


    const report =
        document
        .getElementById(
            "report"+suffix
        )
        .textContent
        .trim();


    if(!report){

        alert("Please generate the report first.");

        return;
    }


    /*
        PRIMARY METHOD:
        Clipboard API.
    */

    try{

        if(
            navigator.clipboard &&
            window.isSecureContext
        ){

            await navigator.clipboard.writeText(
                report
            );

            copiedMessage(button);

            return;
        }

    }catch(error){

        console.log(
            "Clipboard API failed:",
            error
        );
    }


    /*
        FALLBACK METHOD:
        Works on browsers where
        Clipboard API is unavailable.
    */

    try{

        const textarea =
            document.createElement("textarea");


        textarea.value = report;


        textarea.setAttribute(
            "readonly",
            ""
        );


        textarea.style.position =
            "fixed";

        textarea.style.left =
            "-9999px";

        textarea.style.top =
            "0";

        textarea.style.opacity =
            "0";


        document.body.appendChild(
            textarea
        );


        textarea.focus();

        textarea.select();

        textarea.setSelectionRange(
            0,
            textarea.value.length
        );


        const success =
            document.execCommand(
                "copy"
            );


        document.body.removeChild(
            textarea
        );


        if(success){

            copiedMessage(button);

        }else{

            manualCopy(report);

        }

    }catch(error){

        console.log(
            "Fallback copy failed:",
            error
        );

        manualCopy(report);
    }
}



function copiedMessage(button){

    const oldText =
        button.textContent;


    button.textContent =
        "✓ Copied!";


    button.style.background =
        "#16804d";


    setTimeout(
        () => {

            button.textContent =
                oldText;

            button.style.background =
                "";

        },
        1800
    );
}



function manualCopy(text){

    /*
        Last-resort fallback.
        The report is selected so the user
        can use normal Copy.
    */

    const textarea =
        document.createElement("textarea");


    textarea.value =
        text;


    textarea.style.position =
        "fixed";

    textarea.style.left =
        "10px";

    textarea.style.top =
        "10px";

    textarea.style.width =
        "90%";

    textarea.style.height =
        "200px";

    textarea.style.zIndex =
        "99999";


    document.body.appendChild(
        textarea
    );


    textarea.focus();

    textarea.select();


    alert(
        "Automatic copy is unavailable. The report has been selected — tap Copy."
    );
}



function autoLoad(){

    ["second","first"].forEach(
        page => {

            const saved =
                localStorage.getItem(
                    STORAGE[page]
                );


            if(saved){

                const suffix =
                    page === "second"
                    ? "2"
                    : "1";


                const names =
                    JSON.parse(saved);


                document
                    .getElementById(
                        "names"+suffix
                    )
                    .value =
                    names.join("\n");


                data[page].cadets =
                    names.map(name => ({
                        name:name,
                        taps:0,
                        status:"Absent"
                    }));


                render(page);
            }
        }
    );
}


autoLoad();

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )