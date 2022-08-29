# coding: utf-8

# In[1]:

import rebound as rb
import numpy as np
import sys
import reboundx
from reboundx import constants as rbxConstants
import pandas as pd

# set our ICs
date = "2028-05-03 00:00"
DTDIRECT = 1

# solution 2021-Jun-29 11:09:44
# SB441-N16
# epoch 2461894.5 (2028-May-03) TDB
A2 = -2.901085508711e-14  # Yarkovsky parameter
A2SIG = 1.942e-16
betaAsteroid = (
    5e-13 * (365.25 / (2 * np.pi)) ** 2
)  # takes into account radiation effects other than Yarkovsy

twopi = 2 * np.pi

aum = rb.units.lengths_SI["au"]
au = aum * 1e2
aukm = aum / 1e3  # au in km
msun = rb.units.masses_SI["msun"] * 1e3  # grams
code2sec = rb.units.times_SI["yr2pi"]
sec2code = 1.0 / code2sec
vcode2cmps = au * sec2code

A2PARAM = A2 / ((1.0 / 365.25) * np.pi * 2) ** 2  # convert to code units
A2SIGPARAM = A2SIG / ((1.0 / 365.25) * np.pi * 2) ** 2

Rearth = 6371  # km
Vesc = 11.186  # km/s

# used for Earth's J2 component
RE_eq = 6378.135 / aukm
J2 = 1.0826157e-3
J4 = -1.620e-6

dmin = 4.326e-5  # Earth radius in au

tsimend = 0.17  # endtime in years
dtout = 0.17  # end time in years
Noutputs = 200
TMAX = -2.3e9
result = pd.DataFrame()

# Parameter loop lists:
apophis_masses = np.linspace(
    2.2127565415e-20, 3.1179751266e-20, 10
)  # this is a placeholder
vzangles = np.linspace(-16, -10, 7)
vyangle = -5 * twopi / 360
dtfine = 5 * sec2code

masteroid = [
    0,
    63.13,
    17.29,
    13.73,
    5.78,
    2.26,
    2.19,
    2.10,
    1.82,
    1.81,
    1.59,
    1.02,
    0.99,
    0.93,
    0.91,
    0.86,
    0.86,
    0.77,
    0.69,
    0.52,
    0.39,
    0.31,
    0.19,
    0.12,
    0.10,
    0.08,
]
masteroid = np.array(masteroid)
masteroid = masteroid / (aukm**3 * sec2code**2)
print(masteroid)
names = [
    "Sun",
    "Mercury",
    "Venus",
    "Earth",
    "Luna",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Apophis",
    "Ceres",
    "Vesta",
    "Pallas",
    "Hygiea",
    "Davida",
    "Interamnia",
    "Eunomia",
    "A804 RA",
    "Psyche",
    "A858 CA",
    "Thisbe",
    "Sylvia",
    "Hebe",
    "Cybele",
    "A847 PA",
    "Amphitrite",
    "Herculina",
    "Bamberga",
    "Aletheia",
    "Parthenope",
    "Melete",
    "Irene",
    "Aurelia",
    "Ausonia",
    "Hertha",
    "Sat1",
    "Sat2",
]
idEarth = 3
idLuna = 4
idAst = 10
idSat1 = -2
idSat2 = -1
idlist = [idEarth, idAst, idSat1, idSat2]

d1 = 2  # distance from the first satellite to Apophis in km
d2 = 3  # distance from the first satellite to Apophis in km
xa_init = -1.053424570585645  # distance in AU
ya_init = -0.08044494637064198  # distance in AU
za_init = -0.02060117615275531  # distance in AU
vxa_init = (
    0.003081033035886182 * 365.175 / (2 * np.pi)
)  # velocity in AU/year divided by 2pi to match the code
vya_init = (
    -0.01513309275947028 * 365.175 / (2 * np.pi)
)  # velocity in AU/year divided by 2pi to match the code
vza_init = (
    0.000880699780099425 * 365.175 / (2 * np.pi)
)  # velocity in AU/year divided by 2pi to match the code
magv_init = np.sqrt(vxa_init**2 + vya_init**2 + vza_init**2)

scale1 = 1 + d1 / (149597871 * np.sqrt(xa_init**2 + ya_init**2 + za_init**2))
scale2 = 1 + d2 / (149597871 * np.sqrt(xa_init**2 + ya_init**2 + za_init**2))
vscale = (magv_init * 149597871 / (60 * 60 * 24) + 6.4) / (
    magv_init * 149597871 / (60 * 60 * 24)
)


for amass in apophis_masses:
    for zangle in vzangles:
        sim = rb.Simulation()
        sim.integrator = "ias15"
        sim.dt = dtfine  # multiply by negative one for backwards integration

        # epoch 2028 May 03

        sim.add(
            m=0.9999999999950272,
            x=0.0010858861633136002,
            y=-0.002665389484364757,
            z=3.91229617550071e-05,
            vx=9.37502072159369e-05,
            vy=0.00031147119891515774,
            vz=-2.994084669079413e-06,
            hash="Sun",
        )
        sim.add(
            m=1.6601208254808336e-07,
            x=-0.28559306618214686,
            y=0.18553299691422614,
            z=0.04171204295471317,
            vx=-1.2320929034999868,
            vy=-1.298839058813002,
            vz=0.006828227944725816,
            hash="Mercury",
        )
        sim.add(
            m=2.447838287784771e-06,
            x=-0.6575303788722177,
            y=-0.2961045995415499,
            z=0.034007109736063114,
            vx=0.47057150307661444,
            vy=-1.0791099543446236,
            vz=-0.041986232496416774,
            hash="Venus",
        )
        sim.add(
            m=3.0034896154502038e-06,
            x=-0.7397716234503878,
            y=-0.6862856546125479,
            z=8.928236527114675e-05,
            vx=0.6622595974762138,
            vy=-0.7381420479270456,
            vz=7.41963264112652e-05,
            hash="Earth",
        )
        sim.add(
            m=3.694303350091508e-08,
            x=-0.7417786284820342,
            y=-0.6848537655925995,
            z=-1.553213977724315e-05,
            vx=0.642349494064092,
            vy=-0.7675586534333755,
            vz=-0.002641471376982735,
            hash="Luna",
        )
        sim.add(
            m=3.2271560828978514e-07,
            x=1.2729067482670486,
            y=0.6415109809199694,
            z=-0.017639782528535562,
            vx=-0.3364269542361884,
            vy=0.795654921925795,
            vz=0.024918316258483838,
            hash="Mars",
        )
        sim.add(
            m=0.0009547919099366768,
            x=-5.425203852281712,
            y=0.36810152906705407,
            z=0.11990792154710042,
            vx=-0.03496234415319633,
            vy=-0.4172633178008844,
            vz=0.0025163914085928048,
            hash="Jupiter",
        )
        sim.add(
            m=0.0002858856700231729,
            x=7.937717360968882,
            y=4.763669996249208,
            z=-0.39889311226931007,
            vx=-0.18447662495023473,
            vy=0.27741831902497627,
            vz=0.0025201553175330463,
            hash="Saturn",
        )
        sim.add(
            m=4.366249613200406e-05,
            x=6.830306199664484,
            y=18.085344012305832,
            z=-0.021323706314276204,
            vx=-0.21557757282108703,
            vy=0.07012291950757726,
            vz=0.003052920823172897,
            hash="Uranus",
        )
        sim.add(
            m=5.151383772628957e-05,
            x=29.684832728052324,
            y=3.2008686887421702,
            z=-0.7500340539410091,
            vx=-0.020758883575788492,
            vy=0.18251659872024822,
            vz=-0.003280255051013521,
            hash="Neptune",
        )
        sim.add(
            m=amass,
            x=xa_init,
            y=ya_init,
            z=za_init,
            vx=vxa_init,
            vy=vya_init,
            vz=vza_init,
            hash="Apophis",
        )
        sim.add(
            m=4.756901461539691e-10,
            x=-1.8679082509550522,
            y=-1.908238151276263,
            z=0.28341789974043813,
            vx=0.39711153515195774,
            vy=-0.4668509705104752,
            vz=-0.08798714209999689,
            hash="Ceres",
        )
        sim.add(
            m=1.302816826707132e-10,
            x=-2.1358963329567,
            y=1.0205836970040008,
            z=0.22986528849733867,
            vx=-0.22031205490538994,
            vy=-0.6048273772213649,
            vz=0.044777710726456484,
            hash="Vesta",
        )
        sim.add(
            m=1.0345676709478846e-10,
            x=-2.344066748126323,
            y=-0.24573726248030822,
            z=0.3713893748741916,
            vx=-0.01015727857018059,
            vy=-0.5668016185660727,
            vz=0.39399344831159294,
            hash="Pallas",
        )
        sim.add(
            m=4.355281236765312e-11,
            x=-0.8152892331545512,
            y=-2.7079770369874123,
            z=-0.09377572022555405,
            vx=0.5909961692524504,
            vy=-0.19723608531007922,
            vz=0.03549324121964887,
            hash="Hygiea",
        )
        sim.add(
            m=1.7029300337525267e-11,
            x=0.20182683114762695,
            y=-3.7373306446511165,
            z=0.2672657755862881,
            vx=0.44797561569840244,
            vy=0.0315534146976398,
            vz=-0.12472441193423751,
            hash="Davida",
        )
        sim.add(
            m=1.650184413238068e-11,
            x=2.4833777310667693,
            y=-0.058717868010509516,
            z=0.7584856379410004,
            vx=-0.018327845401965276,
            vy=0.6652003694830858,
            vz=0.03090940497471452,
            hash="Interamnia",
        )
        sim.add(
            m=1.582368615433764e-11,
            x=2.0456651865139133,
            y=-1.0508401181838103,
            z=0.30732597946413964,
            vx=0.2102046311081415,
            vy=0.6572347798409284,
            vz=0.09346896571286206,
            hash="Eunomia",
        )
        sim.add(
            m=1.3713861333759286e-11,
            x=-2.0543992794465074,
            y=1.3593484360454189,
            z=-0.22526736891502966,
            vx=-0.48897144398418263,
            vy=-0.4246599982127236,
            vz=0.11642699905468643,
            hash="A804 RA",
        )
        sim.add(
            m=1.363851044731006e-11,
            x=-2.168182047802932,
            y=-2.4310230918743296,
            z=0.17294716272013774,
            vx=0.4131053124523394,
            vy=-0.3165542120894448,
            vz=0.003664677490997351,
            hash="Psyche",
        )
        sim.add(
            m=1.1980790945427069e-11,
            x=-1.7681184888853039,
            y=-2.7247691564364125,
            z=0.40448335337216496,
            vx=0.4178881490953602,
            vy=-0.33597341024381555,
            vz=-0.015382581392147238,
            hash="A858 CA",
        )
        sim.add(
            m=7.685790417821139e-12,
            x=2.401116864261358,
            y=-0.05630114697626136,
            z=0.21766244674071247,
            vx=0.0864636974659242,
            vy=0.6790172041766538,
            vz=0.014672429514757373,
            hash="Thisbe",
        )
        sim.add(
            m=7.459737758473457e-12,
            x=-3.4376287740645646,
            y=-1.360045358256587,
            z=0.5462310146885914,
            vx=0.20321615760469358,
            vy=-0.45012196794210235,
            vz=-0.0632758269406621,
            hash="Sylvia",
        )
        sim.add(
            m=7.007632439778097e-12,
            x=-1.7456578088665409,
            y=-2.0881453540936965,
            z=0.7152522662675125,
            vx=0.45842695523787286,
            vy=-0.29654812459156354,
            vz=-0.021165849078332567,
            hash="Hebe",
        )
        sim.add(
            m=6.856930666879643e-12,
            x=2.6022417130061495,
            y=-1.8363109585524056,
            z=0.035418550543234346,
            vx=0.38339823581242777,
            vy=0.4326947940239929,
            vz=-0.0344958838744026,
            hash="Cybele",
        )
        sim.add(
            m=6.480176234633508e-12,
            x=1.6919767090887123,
            y=-1.4162849782551854,
            z=0.18556413645599462,
            vx=0.316992916731648,
            vy=0.6203052156262215,
            vz=0.019159016128813336,
            hash="A847 PA",
        )
        sim.add(
            m=6.480176234633508e-12,
            x=1.2141385608771758,
            y=2.0196293646004024,
            z=0.22334442698937032,
            vx=-0.5774709100759932,
            vy=0.3441342475184468,
            vz=0.03249510151484477,
            hash="Amphitrite",
        )
        sim.add(
            m=5.8020182565904676e-12,
            x=-1.7269542988742865,
            y=1.5957130421093033,
            z=0.342429974497628,
            vx=-0.37776650818176943,
            vy=-0.5592514340066723,
            vz=0.15434415467320176,
            hash="Herculina",
        )
        sim.add(
            m=5.199211164996652e-12,
            x=-2.834761355602645,
            y=1.5005490440584353,
            z=-0.04655908442465584,
            vx=-0.3445862896546938,
            vy=-0.3501255216210085,
            vz=-0.09414045267652589,
            hash="Bamberga",
        )
        sim.add(
            m=3.918246095359796e-12,
            x=0.6832677623768698,
            y=3.467274059719799,
            z=-0.09253910996740136,
            vx=-0.4790466331494171,
            vy=0.08921382557965962,
            vz=0.0923011965334196,
            hash="Aletheia",
        )
        sim.add(
            m=2.938684571519847e-12,
            x=2.2155339081474414,
            y=0.5334918468769623,
            z=-0.1714362676762051,
            vx=-0.1122781201003882,
            vy=0.6743971705744801,
            vz=-0.024298997015903254,
            hash="Parthenope",
        )
        sim.add(
            m=2.3358774799260323e-12,
            x=-1.994382554230193,
            y=-1.3332089377441085,
            z=0.12228597149838825,
            vx=0.48643480632981734,
            vy=-0.4529283605411481,
            vz=0.078123086047153,
            hash="Melete",
        )
        sim.add(
            m=1.43166684253531e-12,
            x=-5.333034284131448,
            y=0.43147696931576796,
            z=0.08672923729173868,
            vx=0.030451115663884743,
            vy=-0.49306583439932744,
            vz=-0.010072607440351126,
            hash="Irene",
        )
        sim.add(
            m=9.042106373907221e-13,
            x=-1.7656795703791246,
            y=2.527733825029204,
            z=-0.20569814901129932,
            vx=-0.3640823277456266,
            vy=-0.35836598767140554,
            vz=-0.002729954484297129,
            hash="Aurelia",
        )
        sim.add(
            m=7.535088644922685e-13,
            x=-2.2116319831874254,
            y=-0.5986074354912603,
            z=-0.14061492792874822,
            vx=0.25458485286379723,
            vy=-0.6214427794030289,
            vz=-0.048367114889395914,
            hash="Ausonia",
        )
        sim.add(
            m=6.028070915938148e-13,
            x=-0.4147497806129634,
            y=2.6876616287248543,
            z=0.09897386256148458,
            vx=-0.5673613339016015,
            vy=0.010443576274347662,
            vz=-0.0061224144561313676,
            hash="Hertha",
        )

        def rotateZ(vec, eps):
            zr = vec[2] * 1
            xr = vec[0] * np.cos(eps) - vec[1] * np.sin(eps)
            yr = vec[0] * np.sin(eps) + vec[1] * np.cos(eps)
            return np.array([xr, yr, zr])

        def rotateY(vec, eps):
            xr = vec[0] * np.cos(eps) + vec[2] * np.sin(eps)
            yr = vec[1] * 1
            zr = vec[2] * np.cos(eps) - vec[0] * np.sin(eps)
            return np.array([xr, yr, zr])

        satv = rotateZ([vxa_init, vya_init, vza_init], zangle * twopi / 360)
        satv = rotateY(satv, vyangle)

        sim.add(
            m=0.0,
            x=xa_init * scale1,
            y=ya_init * scale1,
            z=za_init * scale1,
            vx=satv[0] * vscale,
            vy=satv[1] * vscale,
            vz=satv[2] * vscale,
            hash="Sat1",
        )
        sim.add(
            m=0.0,
            x=xa_init * scale2,
            y=ya_init * scale2,
            z=za_init * scale2,
            vx=satv[0] * vscale,
            vy=satv[1] * vscale,
            vz=satv[2] * vscale,
            hash="Sat2",
        )

        ps = sim.particles

        Nbod = sim.N

        def rotateX(x, eps):
            xr = x[0] * 1
            yr = x[1] * np.cos(eps) - x[2] * np.sin(eps)
            zr = x[1] * np.sin(eps) + x[2] * np.cos(eps)
            return np.array([xr, yr, zr])

        eps = 23.43651 * twopi / 360.0
        for p in ps:
            x = [p.x, p.y, p.z]
            xr = rotateX(x, eps)
            p.x = xr[0] * 1
            p.y = xr[1] * 1
            p.z = xr[2] * 1
            v = [p.vx, p.vy, p.vz]
            vr = rotateX(v, eps)
            p.vx = vr[0] * 1
            p.vy = vr[1] * 1
            p.vz = vr[2] * 1

        p = ps[idAst]
        p1 = ps[idSat1]
        p2 = ps[idSat2]
        print(
            "sim.add(m={}, x={}, y={}, z={}, vx={}, vy={}, vz={}, A2={} hash='{}')".format(
                p.m, p.x, p.y, p.z, p.vx, p.vy, p.vz, A2PARAM, names[idAst]
            ),
            "sim.add(m={}, x={}, y={}, z={}, vx={}, vy={}, vz={}, A2={} hash='{}')".format(
                p1.m, p1.x, p1.y, p1.z, p1.vx, p1.vy, p1.vz, A2PARAM, names[idSat1]
            ),
            "sim.add(m={}, x={}, y={}, z={}, vx={}, vy={}, vz={}, A2={} hash='{}')".format(
                p2.m, p2.x, p2.y, p2.z, p2.vx, p2.vy, p2.vz, A2PARAM, names[idSat2]
            ),
        )

        rebx = reboundx.Extras(sim)
        gr = rebx.load_force("gr")
        rebx.add_force(gr)
        gr.params["c"] = rbxConstants.C

        mig = rebx.load_force("modify_orbits_forces")  # comment out for A2 = 0
        rebx.add_force(mig)

        gh = rebx.load_force("gravitational_harmonics")
        rebx.add_force(gh)
        ps[idEarth].params["J2"] = J2
        ps[idEarth].params["J4"] = J4
        ps[idEarth].params["R_eq"] = RE_eq

        rf = rebx.load_force("radiation_forces")
        rebx.add_force(rf)
        rf.params["c"] = rbxConstants.C
        ps[idAst].params["beta"] = betaAsteroid

        sim.particles[idEarth].r = dmin  # set size of Earth
        sim.particles[idLuna].r = dmin / 4  # set size of moon

        ps = sim.particles

        ps[idAst].params["tau_a"] = TMAX

        sim.move_to_com()
        # We always move to the center of momentum frame before an integration

        year = 2.0 * np.pi  # One year in units where G=1
        if dtfine < 0:
            times = np.linspace(0.0, -year * tsimend, Noutputs)
            dtout = -dtout * 2 * np.pi
        else:
            times = np.linspace(0.0, year * tsimend, Noutputs)
            dtout = dtout * 2 * np.pi

        # 4 rows, Noutputs columns
        x = np.zeros((4, Noutputs))
        y = np.zeros((4, Noutputs))
        z = np.zeros((4, Noutputs))
        vx = np.zeros((4, Noutputs))
        vy = np.zeros((4, Noutputs))
        vz = np.zeros((4, Noutputs))

        sim.collision = "direct"
        sim.collision_resolve = "merge"
        sim.collision_resolve_keep_sorted = 1
        sim.track_energy_offset = 1

        ps = (
            sim.particles
        )  # ps is now an array of pointers and will change as the simulation runs

        tout = 0
        iout = 0

        for i, time in enumerate(times):
            sim.ri_ias15.epsilon = 0
            sim.dt = dtfine
            print("Check time set: {} s".format(sim.dt * code2sec))
            dadt = (
                2.0
                * A2PARAM
                / (ps[idAst].n * ps[idAst].a ** 2 * (1.0 - ps[idAst].e ** 2))
            )
            TMAX = ps[idAst].a / dadt
            ps[idAst].params["tau_a"] = TMAX
            sim.integrate(time)
            if time % 1:
                sim.save("checkpoint.bin")
            for ind, p in enumerate(idlist):
                x[ind][i] = ps[p].x
                y[ind][i] = ps[p].y
                z[ind][i] = ps[p].z
                vx[ind][i] = ps[p].vx
                vy[ind][i] = ps[p].vy
                vz[ind][i] = ps[p].vz

        distancesat1 = (
            np.sqrt(
                np.square(x[2] - x[1]) + np.square(y[2] - y[1]) + np.square(z[2] - z[1])
            )
            * aukm
        )

        distancesat2 = (
            np.sqrt(
                np.square(x[3] - x[1]) + np.square(y[3] - y[1]) + np.square(z[3] - z[1])
            )
            * aukm
        )

        diff_distsat = distancesat2 - distancesat1

        distancebtwnsats = (
            np.sqrt(
                np.square(x[3] - x[2]) + np.square(y[3] - y[2]) + np.square(z[3] - z[2])
            )
            * aukm
        )
        dfx = pd.DataFrame(x)
        dfx[["rowtype", "vi_angle", "Apophis_mass"]] = "x", zangle, amass
        dfy = pd.DataFrame(y)
        dfy[["rowtype", "vi_angle", "Apophis_mass"]] = "y", zangle, amass
        dfz = pd.DataFrame(z)
        dfz[["rowtype", "vi_angle", "Apophis_mass"]] = "z", zangle, amass
        dfdist1 = pd.DataFrame([distancesat1])
        dfdist1[["rowtype", "vi_angle", "Apophis_mass"]] = (
            "dist1",
            zangle,
            amass,
        )
        dfdist2 = pd.DataFrame([distancesat2])
        dfdist2[["rowtype", "vi_angle", "Apophis_mass"]] = (
            "dist2",
            zangle,
            amass,
        )
        dfdistdiff = pd.DataFrame([diff_distsat])
        dfdistdiff[["rowtype", "vi_angle", "Apophis_mass"]] = (
            "distdiff",
            zangle,
            amass,
        )
        dfbtwnsats = pd.DataFrame([distancebtwnsats])
        dfbtwnsats[["rowtype", "vi_angle", "Apophis_mass"]] = (
            "distbtwnsats",
            zangle,
            amass,
        )
        result = pd.concat(
            [result, dfx, dfy, dfz, dfdist1, dfdist2, dfdistdiff, dfbtwnsats]
        )


result.to_csv("osi_sat_sim_results_closer.csv", index=False)
