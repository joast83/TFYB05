"""Student-facing starting equations. Share notation across related exercises."""
LAWS = {}


def _law(ids, name, equation, prompt):
    for pid in ids.split():
        if pid in LAWS:
            raise ValueError(pid)
        LAWS[pid] = (name, equation, prompt)


_law("2.1 4.3 7.7", "Kraftjämvikt", r"\sum_i \mathbf F_i=\mathbf 0", "Kroppen är i vila. Rita en pil för varje kraft och välj sedan en riktning att skriva kraftbalansen i.")
_law("2.2 2.3 2.4", "Coulombs lag", r"\mathbf E(\mathbf r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\mathbf r-\mathbf r'}{|\mathbf r-\mathbf r'|^3}\,\mathrm dQ'", "Laddningen är utspridd. Tänk dig en liten bit med laddningen dQ′ vid källpunkten r′. Fältpunkten r ligger still. Vilken koordinat behöver du variera för att gå igenom hela källan?")
_law("2.5 2.16", "Elektrisk potential", r"V(\mathbf r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\mathrm dQ'}{|\mathbf r-\mathbf r'|}", "Välj nollpotential vid oändligheten. Var finns laddningen och hur långt är det från varje källelement till fältpunkten?")
_law("2.6 2.7 2.8 2.11 2.12 2.18 4.5", "Gauss lag", r"\oint_S\mathbf E\cdot\mathrm d\mathbf S=\frac{Q_{\mathrm{in}}}{\varepsilon_0}", "Välj en sluten yta. Var är fältets normalkomponent konstant eller noll på grund av symmetrin? Räkna bara laddningen innanför ytan.")
_law("2.9", "Gauss lag", r"Q_{\mathrm{in}}=\varepsilon_0\oint_S\mathbf E\cdot\mathrm d\mathbf S", "Här är fältet känt och laddningen söks. Markera utåtnormalerna på cylinderns topp och botten.")
_law("2.10 3.1", "Superpositionsprincipen", r"\mathbf E(\mathbf r)=\sum_i\mathbf E_i(\mathbf r)", "Vilka källor kan du beräkna fältet från var för sig? Summera deras vektorer i samma observationspunkt.")
_law("2.13 2.19", "Gauss lag i differentialform", r"\nabla\cdot\mathbf E=\rho/\varepsilon_0,\qquad \Delta V=-\int\mathbf E\cdot\mathrm d\boldsymbol\ell", "Vilken koordinat varierar fältet med? Laddningstätheten bestämmer divergensen och randvillkoren bestämmer integrationskonstanterna.")
_law("3.3 3.6 3.7 3.9 3.12 3.14", "Gauss lag för D", r"\oint_S\mathbf D\cdot\mathrm d\mathbf S=Q_{\mathrm{fri,in}},\qquad \mathbf D_i=\varepsilon_0\varepsilon_{r,i}\mathbf E_i", "Identifiera fri laddning och dela upp ytan efter material. Använd materialets relativa permittivitet tillsammans med ε₀. Vilken fältkomponent bidrar till flödet?")
_law("3.11 3.13", "Potentialskillnad och genomslag", r"\Delta V=-\int\mathbf E\cdot\mathrm d\boldsymbol\ell,\qquad |\mathbf E_i|\le E_{i,\max}", "Vilka material passerar vägen mellan plattorna? Varje material har sin egen fältgräns.")
_law("3.18", "Bundna laddningar", r"\rho_b=-\nabla\cdot\mathbf P,\qquad \sigma_b=\mathbf P\cdot\hat{\mathbf n}", "Bestäm först vilka ytor eller volymer som faktiskt bär laddning. Använd sedan Coulombs lag för dessa källor.")
_law("3.19 5.15", "Elektriska randvillkor", r"\hat{\mathbf n}\cdot(\mathbf D_2-\mathbf D_1)=\sigma_{\mathrm{fri}},\qquad \mathbf E_{2t}=\mathbf E_{1t}", "Välj normalen från medium 1 till 2. Dela upp fälten i normal- och tangentialkomponenter innan du använder villkoren.")
_law("4.1", "Uppladdningsarbete", r"W=\int_0^Q[V(q)-V(\infty)]\,\mathrm dq", "Vad är skalets potential när bara laddningen q har förts dit?")
_law("4.2", "Elektriskt tryck", r"p=\varepsilon_0 E_n^2/2,\qquad F=pA", "Identifiera fältet i luften precis utanför plattan och arean som trycket verkar på.")
_law("4.6", "Energibalans", r"V_0\,\mathrm dQ=\mathrm d(CV_0^2/2)+F_x\,\mathrm dx", "Vad håller spänningskällan konstant när dielektrikumet flyttas?")
_law("4.7", "Spegelladdningsmetoden", r"V(\mathbf r)=\sum_i\frac{q_i}{4\pi\varepsilon_0|\mathbf r-\mathbf r_i|}", "Vilken hjälpladdning ger noll potential i varje punkt på det jordade planet?")
_law("5.1 5.7", "Stationär ström och Ohms lag", r"I=\int_S\mathbf J\cdot\mathrm d\mathbf S,\qquad \mathbf J=\sigma\mathbf E", "Samma ström passerar varje koaxial cylinderyta. Vilka av area och konduktivitet beror på radien?")
_law("5.2 5.10", "Ohms lag", r"R=U/I,\qquad R_{\mathrm{bana}}=\ell/(\sigma A)", "Identifiera längd och tvärsnitt längs strömvägen. Passerar samma ström alla delar, eller har banorna samma spänning?")
_law("6.1 6.2 6.3 6.8", "Biot–Savarts lag", r"\mathbf B(\mathbf r)=\frac{\mu_0 I}{4\pi}\int\frac{\mathrm d\boldsymbol\ell'\times(\mathbf r-\mathbf r')}{|\mathbf r-\mathbf r'|^3}", "Välj en koordinat som följer ledaren i strömriktningen. Skriv linjeelementet och separationsvektorn i samma bas före korsprodukten.")
_law("6.5 6.13", "Superposition av strömbidrag", r"\mathbf B=\int\mathrm d\mathbf B", "Dela källan i enkla strömbanor. Hur mycket ström bär varje bana, och vilket fält ger den i observationspunkten?")
_law("7.1", "Magnetiskt dipolmoment", r"\mathbf m=IA\hat{\mathbf n},\qquad I=q/\tau", "Bestäm omloppstiden och skilj elektronens rörelseriktning från den konventionella strömmens riktning.")
_law("7.2", "Vridmoment på en strömslinga", r"\mathrm d\mathbf F=I\,\mathrm d\boldsymbol\ell\times\mathbf B,\qquad \mathbf T=\oint\mathbf r\times\mathrm d\mathbf F", "Skilj hävarmen från linjeelementet. Båda ändrar riktning längs slingan.")
_law("7.3", "Vridmoment på en magnetisk dipol", r"\mathbf T_2=\mathbf m_2\times\mathbf B_1", "Beräkna den första dipolens fält vid den andra dipolen. Vilken fältkomponent ger ett moment?")
_law("7.5", "Relativt fel", r"\delta=|B_{\mathrm{dip}}-B_{\mathrm{exakt}}|/|B_{\mathrm{exakt}}|", "Jämför båda fälten i samma punkt. Vilket fält ska stå i nämnaren?")
_law("7.6 7.10 8.6", "Magnetiskt flöde", r"\Phi=\int_S\mathbf B\cdot\mathrm d\mathbf S", "Välj yta och normal. Är normalkomponenten konstant över ytan eller måste den integreras?")
_law("8.1 8.2 8.4 8.5 8.13", "Ampères cirkulationslag", r"\oint_C\mathbf H\cdot\mathrm d\boldsymbol\ell=I_{\mathrm{fri,in}}", "Välj integrationsväg och identifiera den fria ström den omsluter. I vilka delar av vägen kan H behandlas som konstant?")
_law("8.12", "Bundna strömmar", r"\mathbf J_m=\nabla\times\mathbf M,\qquad \mathbf K_m=\mathbf M\times\hat{\mathbf n}", "Vad ger en konstant magnetisering inne i volymen? Pröva sedan utåtnormalen på varje yta.")
_law("9.2 9.4", "Ömsesidig induktans", r"M=\Phi_2/I_1,\qquad \Phi_2=\int_{S_2}\mathbf B_1\cdot\mathrm d\mathbf S", "Identifiera källslingan och mottagarslingans orienterade yta. Varierar fältet över mottagaren?")
_law("9.6 9.13 9.14", "Faradays induktionslag", r"\mathcal E=-\frac{\mathrm d(N\Phi)}{\mathrm dt}", "Välj slingnormal och positiv omloppsriktning tillsammans. Vilken del av flödet per varv ändras med tiden?")
_law("10.2", "Förskjutningsström", r"\mathbf J_F=\partial\mathbf D/\partial t", "Koppla plattans fria laddning till D och använd strömmen för att bestämma laddningens tidsderivata.")
_law("10.3", "Gauss lag för magnetfältet", r"\oint_S\mathbf B\cdot\mathrm d\mathbf S=0", "Börja med del (a): vilken riktning skulle fältet kunna ha enligt sfärisk symmetri? Pröva den på en sluten sfär.")
