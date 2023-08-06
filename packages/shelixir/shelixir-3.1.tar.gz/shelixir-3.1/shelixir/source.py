#!/usr/bin/python3

import os
import argparse
import textwrap
import re
import sys
import multiprocessing as mp
import shutil

cell = []
list_of_files = []
progress = 0
list = []

print("""
##################################################
#
# SHELIXIR in Python 3
#
# https://kmlinux.fjfi.cvut.cz/~kolenpe1/shelixir
# kolenpe1@cvut.cz
##################################################
""")





##################################################
# PARSING ARGUMENTS
##################################################


parser=argparse.ArgumentParser(
    prog='SHELIXIR',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''\

    List of Bravais types:
    aP: P1
    mP: P2, P21
    mC: C2
    oP: P222, P2221, P21212, P212121
    oC: C222, C2221
    oF: F222
    oI: I222, I212121
    tP: P4, P41, P42, P43, P422, P4212, P4122, P41212, P4222, P42212, P4322, P43212
    tI: I4, I41, I422, I4122
    hP: P3, P31, P32, P312, P321, P3112, P3121, P3212, P3221, P6, P61, P65, P62, P64, P63, P622, P6122, P6522, P6222, P6422, P6322
    hR: R3, R32
    cP: P23, P213, P432, P4232, P4332, P4132
    cF: F23, F432, F4132
    cI: I23, I213, I432, I4132

    Most frequent SHELXE parameters:
    -h  heavy atoms are included in the native structure
    -hN when the number N of heavy atoms is known
    -aN runs N cycles of auto-tracing
    -q  explicit search for helices
    -s  fraction of solvent content(e.g. -s0.45)
    -e  runs free lunch algorithm (e.g. -e1.2)
    -z  optimizes the heavy atom substructure before the density modification

    '''))
parser.add_argument("-pref", "--prefix", help="name of the project", type=str)
parser.add_argument("-wdir", "--working_directory", \
    help="path to the working directory, MUST EXIST!", type=str)
parser.add_argument("-s", "--sad", help="SAD dataset", type=str)
parser.add_argument("-n", "--nat", help="native dataset", type=str)
parser.add_argument("-p", "--peak", help="peak dataset", type=str)
parser.add_argument("-i", "--infl", help="inflection point dataset", type=str)
parser.add_argument("-hr", "--hrem", help="high remote dataset", type=str)
parser.add_argument("-lr", "--lrem", help="low remote dataset", type=str)
parser.add_argument("-b", "--before", help="BEFORE dataset for RIP", type=str)
parser.add_argument("-a", "--after", help="AFTER dataset for RIP", type=str)
parser.add_argument("-sa", "--sira", help="SIRAS dataset", type=str)
parser.add_argument("-seq", "--sequence_file", help="Amino acid sequence",    \
    type=str)
parser.add_argument("-nproc", help="number of processes to parallelize",      \
    type=int)
parser.add_argument("-res", help="low and high resolution limits for phasing",\
    type=float, nargs='+')
parser.add_argument("-sfac", help="heavy elements, e.g. Se, Gd, etc.",        \
    type=str)
parser.add_argument("-find", help="number of searched atoms", type=int)
parser.add_argument("-ntry",                                                  \
    help="number of trials to search for substructure", type=int)
parser.add_argument("-mind", help="minimal distance between the heavy atoms", \
    type=str)
parser.add_argument("-bt", "--bravais", help="selection of Bravais type",     \
    type=str)
parser.add_argument("-l", "--list",                                           \
    help="list of manually chosen space groups", type=str, nargs='+')
parser.add_argument("-c", "--cell", type=int, help="unit cell parameters",    \
    nargs='+')
parser.add_argument("-w", "--wavelength", type=float,                         \
    help="wavelength of the primary beam")
parser.add_argument("-Epar", "--SHELXE_parameters", type=str,                 \
    help="parameters for SHELXE, use as -Epar=\"parameters\"")#, nargs='+')
parser.add_argument("-Ebin", "--SHELXE_binary", type=str,                     \
    help="path to SHELXE binary file")
parser.add_argument("-cc", "--CFOM_cutoff",                                   \
    help="cutoff to be applied after SHELXD procedure", type=float)
parser.add_argument("-ss", "--solvent_screen",                                \
    help="solvent screening,  minimal and maximal solvent " +                 \
    "content and steps for screening", type=int, nargs='+')                 
parser.add_argument("-ss_auto", "--screen_solvent_automatic",                 \
    help="automatic solvent screen", action='store_true')
parser.add_argument("-ss_m", "--solvent_manual",                              \
    help="manual entries for solvent screening", type=int, nargs='+')
parser.add_argument("-sh", "--screen_high",                                   \
   help="variants of high resolution limit", type=str, nargs='+')
parser.add_argument("-sl", "--screen_low",                                    \
    help="variants of low resolution limit", type=str, nargs='+')
parser.add_argument("-mr", "--molecular_replacement",                         \
    help="model after molecular replacement", type=str)
args = parser.parse_args()

##################################################
# CHECKING FOR BINARIES AND SOFTWARE AVAILABILITY
##################################################

def isBinary(binary):
    if path := shutil.which(binary):
        print("Path to binary: "+ path)
    else:
        print(binary+" is unavailable. Exiting ...")
        exit()

binaries = ('shelxc', 'shelxd', 'shelxe')
for i in binaries:
    isBinary(i)

if args.SHELXE_binary:
    bine = os.path.abspath(args.SHELXE_binary)
    print("SHELXE binary is here: " + bine)
else:
    bine = shutil.which('shelxe')

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print("The module Matplotlib is not installed.\n") 
    quit()
else:
    pass


##################################################
# BASIC VARIABLE ASSIGNMENT
##################################################

# CHECKING FOR CORRECT PREFIX
if not args.prefix:
    print('Prefix not set. Exiting ...')
    exit()

# CHECKING FOR NUMBER OF PARALLEL PROCESSES
if args.nproc:
    nproc = args.nproc
    print("Number of parallel processes: {}".format(nproc))
else:
    nproc = mp.cpu_count()
    print("Number of parallel processes: {}".format(nproc))

# WAVELENGTH SETTING
if not args.wavelength:
    args.wavelength = 0.98


# SOLVENT SCREENING VS. STANDARD SHELXE RUN
if args.screen_solvent_automatic:
    print('Standard solvent screen on.')
    args.solvent_screen = [20, 80, 5]

if args.solvent_screen:
    print('Solvent screen on.')
    if len(args.solvent_screen) != 3:
        print('Incorrect number of solvent screening parameters. Exiting ...')
        exit()
    if args.solvent_screen[0] >= args.solvent_screen[1]:
        print('Incorrect solvent screening parameters.\n'                     \
            + ' Please check the input. Exiting ...')
        exit()
    actual_solvent = args.solvent_screen[0]
    # initializes list of solvent
    solvent_list = []
    # initializes list of screening atoms original
    screening_atoms_original = []
    # initializes list of screening atoms inverted
    screening_atoms_inverted = []
    # initializes list of contrasts for original hand
    screening_contrast_original = []
    # initializes list of contrasts for inverted hand
    screening_contrast_inverted = []
    # initializes list of connectivity for original hand
    screening_connectivity_original = []
    # initializes list of connectivity for inverted hand
    screening_connectivity_inverted = []
    # FILLING OF MATRICES WITH ZEROS
    while actual_solvent <= args.solvent_screen[1]:
        solvent_list.append(actual_solvent)
        # init of screening atoms original
        screening_atoms_original.append(0)         
        # init of screening atoms inverted
        screening_atoms_inverted.append(0)         
        # init of contrasts for original hand
        screening_contrast_original.append(0)      
        # init of contrasts for inverted hand
        screening_contrast_inverted.append(0)      
        # init of connectivity for original hand
        screening_connectivity_original.append(0)  
        # init of connectivity for inverted hand
        screening_connectivity_inverted.append(0)  
        actual_solvent = actual_solvent + args.solvent_screen[2]
    actual_solvent = args.solvent_screen[0]
# Initialization of working lists
else:
    standard_atoms = [0, 0]           # working number of atoms
    


##################################################
# PREPARATION AND GOING TO WORKING DIRECTORY
##################################################

if args.working_directory:     #checks where the working directory is ...
    args.working_directory = os.path.abspath(args.working_directory)
else:
    args.working_directory = os.getcwd()


if os.path.isdir(args.working_directory + "/shelixir_" + args.prefix):
    print("Working directory " + args.working_directory + "/shelixir_"        \
        + args.prefix + " exists. Exiting ...")
    exit()
else:
    os.mkdir(args.working_directory + '/shelixir_' + args.prefix)
    print("Working directory: " + args.working_directory + "/shelixir_"       \
        + args.prefix)


##################################################
# MAKING LIST OF FILES FOR SHELXC
##################################################

c_file = ['CELL ', 'SPAG ']

if args.sad:
    args.sad = os.path.abspath(args.sad)
    sad = os.path.basename(args.sad)
    print("SAD is defined as {}.".format(args.sad))
    cellFile = args.sad
    list_of_files.append('SAD')
    os.system('cp ' + args.sad + ' ' + args.working_directory + '/shelixir_'  \
        + args.prefix + '/sad-' + sad)
    sad = 'sad-' + sad
    c_file.append('SAD ' + sad)

if args.nat:
    args.nat = os.path.abspath(args.nat)
    nat = os.path.basename(args.nat)
    if args.molecular_replacement:
        if args.molecular_replacement:
            cellFile = args.nat
        else:
            print('Model from molecular replacement is not set. Exiting ...')
    print("Native dataset is defined as {}.".format(args.nat))
    os.system('cp ' + args.nat + ' ' + args.working_directory + '/shelixir_'  \
        + args.prefix + '/nat-' + nat)
    nat = 'nat-' + nat
    c_file.append('NAT ' + nat)

if args.peak:
    args.peak = os.path.abspath(args.peak)
    peak = os.path.basename(args.peak)
    print("Peak dataset is defined as {}.".format(args.peak))
    cellFile = args.peak
    list_of_files.append('PEAK')
    os.system('cp ' + args.peak + ' ' + args.working_directory + '/shelixir_' \
        + args.prefix + '/peak-' + peak)
    peak = 'peak-' + peak
    c_file.append('PEAK ' + peak)

if args.infl:
    args.infl = os.path.abspath(args.infl)
    infl = os.path.basename(args.infl)
    print("Inflection dataset is defined as {}.".format(args.infl))
    list_of_files.append('INFL')
    os.system('cp ' + args.infl + ' ' + args.working_directory + '/shelixir_' \
        + args.prefix + '/infl-' + infl)
    infl = 'infl-' + infl
    c_file.append('INFL ' + infl)

if args.hrem:
    args.hrem = os.path.abspath(args.hrem)
    hrem = os.path.basename(args.hrem)
    print("High-remote dataset is defined as {}.".format(args.hrem))
    list_of_files.append('HREM')
    os.system('cp ' + args.hrem + ' ' + args.working_directory + '/shelixir_' \
        + args.prefix + '/hrem-' + hrem)
    hrem = 'hrem-' + hrem
    c_file.append('HREM ' + hrem)

if args.lrem:
    args.lrem = os.path.abspath(args.lrem)
    lrem = os.path.basename(args.lrem)
    print("Low remote dataset is defined as {}.".format(args.lrem))
    list_of_files.append('LREM')
    os.system('cp ' + args.lrem + ' ' + args.working_directory + '/shelixir_' \
        + args.prefix + '/lrem-' + lrem)
    lrem = 'lrem-' + lrem
    c_file.append('LREM ' + lrem)

if args.before:
    args.before = os.path.abspath(args.before)
    before = os.path.basename(args.before)
    print("BEFORE dataset for RIP is defined as {}.".format(args.before))
    cell_file = args.before
    list_of_files.append('BEFORE')
    os.system('cp ' + args.before + ' ' + args.working_directory              \
        + '/shelixir_' + args.prefix + '/before-' + before)
    before = 'before-' + before
    c_file.append('BEFORE ' + before)

if args.after:
    args.after = os.path.abspath(args.after)
    after = os.path.basename(args.after)
    print("AFTER dataset for RIP is defined as {}.".format(args.after))
    list_of_files.append('AFTER')
    os.system('cp ' + args.after + ' ' + args.working_directory               \
        + '/shelixir_' + args.prefix + '/after-' + after)
    after = 'after-' + after
    c_file.append('AFTER ' + after)

if args.sira:
    args.sira = os.path.abspath(args.sira)
    sira = os.path.basename(args.sira)
    print("SIRAS dataset is defined as {}.".format(args.sira))
    cellFile = args.sira
    list_of_files.append('SIRA')
    os.system('cp ' + args.sira + ' ' + args.working_directory + '/shelixir_' \
        + args.prefix + '/sira-' + sira)
    sira = 'sira-' + sira
    c_file.append('SIRA ' + sira)
    
if args.molecular_replacement:
    args.molecular_replacement = os.path.abspath(args.molecular_replacement)
#    mr = os.path.basename(args.molecular_replacement)
    print("MR modelis defined as {}.".format(args.molecular_replacement))
    os.system('cp ' + args.molecular_replacement + ' '                        \
        + args.working_directory + '/shelixir_' + args.prefix + '/mr-'        \
        + args.prefix + '.pda')
    if not args.nat:
        print('Native data is not set. Exiting ...')
        exit()
    os.system('cp ' + args.nat + ' ' + args.working_directory + '/shelixir_'  \
        + args.prefix + '/mr-' + args.prefix + '.hkl')
    if not args.SHELXE_parameters:
        print('Define SHELXE parameters. Exiting ...')
        exit()

if args.sequence_file:
    args.sequence_file = os.path.abspath(args.sequence_file)

print('Unit cell parameters are derived from file: ' + cellFile )

os.chdir(args.working_directory + '/shelixir_' + args.prefix)

##################################################
# READING UNIT CELL PARAMETERS
##################################################

# READING FROM XDS *.HKL FILE
def read_hkl_file():
    global c_file, cell
    if '.HKL' in cellFile:
        file = open(cellFile, 'r')
        for line in file.readlines():
            if re.search('!UNIT_CELL_CONSTANTS', line):
    #            print(line.split()[1:7])
                for i in range(6):
                    cell.append(float(line.split()[i+1]))
            if re.search('X-RAY_WAVELENGTH=', line):
                args.wavelength = line.split()[1]
            file.close()
    if '.sca' in cellFile:
        file = open(cellFile, 'r')
        work_cell = file.readlines()[2].split()
        file.close()
        for i in range(6):
            cell.append(float(work_cell[i]))
    
    if len(cell) != 6:
        print('Incorrect number of unit-cell parameters. Exiting ...')
        exit()
    else:
        print(cell)
    
    if args.cell:
        if len(args.cell) != 6:
            print('Incorrect number of unit cell parameters. '                \
                + 'Please, check the input.')
            exit()
        else:
            print('Number of unit cell parameters is: ', int(len(args.cell)))
            print("Unit cell parameters are: "                                \
                + "{}, {}, {}, {}, {}, {}".format(args.cell[0],\
                args.cell[1], args.cell[2], args.cell[3], args.cell[4],       \
                args.cell[5]))
            cell = args.cell
    
    c_file[0] = 'CELL ' + str(args.wavelength) + ' ' + str(cell[0]) + ' '     \
        + str(cell[1]) + ' ' + str(cell[2]) + ' ' + str(cell[3]) + ' '        \
        + str(cell[4]) + ' ' + str(cell[5])






##################################################
# APPENDING IMPORTANT INFORMATION FOR SHELXC INPUT
def c_file_append():
    global c_file
    if args.ntry:
        c_file.append('NTRY ' + str(args.ntry))
    else:
        c_file.append('NTRY 100')
    
    if not args.sfac:
        args.sfac = "Se"
    print("Heavy element: {}.".format(args.sfac))
    c_file.append('SFAC ' + args.sfac)
    
    if not args.find:
        args.find = 10
    print("Number of heavy atoms to be found: {}.".format(args.find))
    c_file.append('FIND ' + str(args.find))
    
    if args.res:
        if len(args.res) != 2:
            print('Incorrect number of resolution limits. Please, check the ' \
                + 'input.')
            exit()
        else:
            print("Resolution for phasing: "                                  \
                + "{}, {}.".format(args.res[0], args.res[1]))
            c_file.append('SHEL ' + str(args.res[0]) + ' ' + str(args.res[1]))


##################################################
# SPACE GROUP DEFINITION
##################################################

def sg_list_generation():
    global list
    if args.bravais:
        if args.bravais == 'aP':
            list = ['P1']
        elif args.bravais == 'mP':
            list = ['P2', 'P21']
        elif args.bravais == 'mC':
            list = ['C2']
        elif args.bravais == 'oP':
            list = ['P222', 'P2221', 'P2212', 'P2122', 'P22121', 'P21221',    \
                'P21212', 'P212121']
        elif args.bravais == 'oC':
            list = ['C222', 'C2221']
        elif args.bravais == 'oF':
            list = ['F222']
        elif args.bravais == 'oI':
            list = ['I222', 'I212121']
        elif args.bravais == 'tP':
            list = ['P4', 'P41', 'P42', 'P43', 'P422', 'P4212', 'P4122',      \
                'P41212', 'P4222', 'P42212', 'P4322', 'P43212']
        elif args.bravais == 'tI':
            list = ['I4', 'I41', 'I422', 'I4122']
        elif args.bravais == 'hP':
            list = ['P3', 'P31', 'P32', 'P312', 'P321', 'P3112', 'P3121',     \
                'P3212', 'P3221', 'P6', 'P61', 'P65', 'P62', 'P64', 'P63',    \
                'P622', 'P6122', 'P6522', 'P6222', 'P6422', 'P6322']
        elif args.bravais == 'hR':
            list = ['R3', 'R32']
        elif args.bravais == 'cP':
            list = ['P23', 'P213', 'P432', 'P4232', 'P4332', 'P4132']
        elif args.bravais == 'cF':
            list = ['F23', 'F432', 'F4132']
        elif args.bravais == 'cI':
            list = ['I23', 'I213', 'I432', 'I4132']
        else:
            print('Unrecognized Bravais type.')
            exit()
    # USER HAS DEFINED OWN LIST OF SPACE GROUPS
    if args.list:
        print("Space gropus to be tested: {}".format(args.list))
        list = args.list
    if not list:
        if not args.molecular_replacement:
            print('Space groups are not defined. Exiting ...')
            exit()




##################################################
# HTML output
##################################################

references = ['<h2>References</h2>\n', '<p>\n',
        'P. Kolenko, J. Stransky, T. Koval, M. Maly, J. Dohnalek. (2021).'    \
        + ' SHELIXIR: automation of experimental phasing procedures using'    \
        + ' SHELXC/D/E. <i>J. Appl. Cryst.</i>, <b>54</b>,'                   \
        + ' https://doi.org/10.1107/S1600576721002454.\n', '</p>\n',
        '<p>\n', 'Please cite: I. Uson & G.M. Sheldrick (2018),'              \
        + ' An introduction to experimental phasing of macromolecules'        \
        + ' illustrated by SHELX; new autotracing features" Acta Cryst. D74,' \
        + ' 106-116 (Open Access) if SHELXE proves useful.\n', '</p>\n']



html_all = []
def html_init():
    global html_head1, cell, html_all
    html_head1 = ['<HTML>\n', '<head>\n', '<meta charset="utf-8">\n', 
        '<style>\n', 'table {border-spacing: 0; border-collapse: separate;}\n', 
        'td {padding: 0;}\n', 
        'hr {border: 1px solid grey:}\n',
        'span.sg {font-weight: bold; padding: 4px; border-style: solid;       \
        border-width: 3px; border-radius: 1ex;}\n',
        'div.sg {padding-left: 1ex; border-left-style: solid;                 \
        border-left-width: 1ex}\n',
        '.sg:nth-of-type(8n+1) {border-color: red;}\n',
        '.sg:nth-of-type(8n+2) {border-color: orange;}\n',
        '.sg:nth-of-type(8n+3) {border-color: green;}\n',
        '.sg:nth-of-type(8n+4) {border-color: blue;}\n',
        '.sg:nth-of-type(8n+5) {border-color: magenta;}\n',
        '.sg:nth-of-type(8n+6) {border-color: purple;}\n',
        '.sg:nth-of-type(8n+7) {border-color: grey;}\n',
        '.sg:nth-of-type(8n) {border-color: SaddleBrown;}\n',
        '@media print {#ghostery-purple-box {display:none !important}}        \
        </style>\n',
        '<meta http-equiv="refresh" content="10">', '<title>Project</title>\n', 
        '</head>\n', '<body>\n',
        '<h1 align="center"><i>SHELIXIR</i> - ' + args.prefix + '</h1>\n', 
        '<h2>Settings:</h2>\n', '<table cellpadding="3">\n',
        '<tr><td>Status:</td><td bgcolor="orange">running ...</td></tr>\n',
        '<tr><td>Input files</td><td></td></tr>\n']
    if args.sad:
        html_head1.append('<tr><td>SAD file:</td><td>' + args.sad             \
            + '</td></tr>\n')
    if args.sira:
        html_head1.append('<tr><td>SIRA file:</td><td>' + args.sira           \
            + '</td></tr>\n')
    if args.peak:
        html_head1.append('<tr><td>PEAK file:</td><td>' + args.peak           \
            + '</td></tr>\n')
    if args.infl:
        html_head1.append('<tr><td>INFL file:</td><td>' + args.infl           \
            + '</td></tr>\n')
    if args.hrem:
        html_head1.append('<tr><td>HREM file:</td><td>' + args.hrem           \
            + '</td></tr>\n')
    if args.lrem:
        html_head1.append('<tr><td>LREM file:</td><td>' + args.lrem           \
            + '</td></tr>\n')
    if args.nat:
        html_head1.append('<tr><td>NAT file:</td><td>' + args.nat 
            + '</td></tr>\n')
    if args.before:
        html_head1.append('<tr><td>BEFORE file:</td><td>' + args.before       \
            + '</td></tr>\n')
    if args.after:
        html_head1.append('<tr><td>AFTER file:</td><td>' + args.after         \
            + '</td></tr>\n') 
    html_head1.append('<tr><td width="250">Unit cell parameters: </td><td>'   \
        + str(cell[0]) + ' ' + str(cell[1]) + ' ' + str(cell[2]) + ' '        \
        + str(cell[3]) + ' ' + str(cell[4]) + ' ' + str(cell[5])              \
        + '</td></tr>\n')
    html_head1.append('<tr><td>Wavelength:</td><td>' + str(args.wavelength)   \
        + '</td></tr>\n')
    html_head1.append('<tr><td>Atoms to be found:</td><td>' + str(args.find)  \
        + '</td></tr>\n')
    html_head1.append('<tr><td>Number of trials:</td><td>' + str(args.ntry)   \
        + '</td></tr>\n')
    html_head1.append('<tr><td>ShelxE parameters:</td><td>'                   \
        + str(args.SHELXE_parameters) + '</td></tr>\n')
    html_head1.append('</table>\n')
    html_head1.append('<p>\n')
    
    for i in range(len(list)):
        html_head1.append('- <span class="sg"><a href="#' + str(list[i])      \
            + '">' + str(list[i]) + '</a></span> - \n')
    
    html_head1.append('</p>\n')

def write_html_cfiles(space_group, prefix):
    html_all.append('<div class="sg">\n')
    html_all.append('<h2 id="' + str(space_group) + '">Trial in space group ' \
        + str(space_group) + '</h2>\n')
    html_all.append('<h3>SHELXC</h3>\n')
    html_all.append('<p>\n')
    # Input of SHELXC files
    if os.path.isfile(space_group + '_' + str(prefix) + '_shelxc.inp'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            + '_shelxc.inp">' + space_group + '_' + str(prefix)               \
            + '_shelxc.inp</a> - ')
    if os.path.isfile(space_group + '_' + str(prefix) + '_shelxc.log'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            +'_shelxc.log">' + space_group + '_' + str(prefix)                \
            +'_shelxc.log</a> <br>')
    html_all.append('\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_shelxc.png'):
        html_all.append('<img src="' + space_group + '_' + str(prefix)        \
            + '_shelxc_detail.png"> <br>\n')
    # Read the resolution from the _fa.ins file and put it to the HTML
    if os.path.isfile(space_group + '_' + str(prefix) + '_fa.ins'):
        with open(space_group + '_' + prefix + '_fa.ins', "r") as din:
            lines = din.readlines()
        for j in range(len(lines)):
            if "SHEL" in lines[j]:
                html_all.append('Current resolution is: '                     \
                    + str(float(lines[j].split()[1])) + ' '                   \
                    + str(float(lines[j].split()[2])) + '.\n')
    html_all.append('</p>\n')

def write_html_dfiles(space_group, prefix):
    html_all.append('<h3>SHELXD</h3>\n')
    html_all.append('<p>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_fa.ins'):
        html_all.append('<a href="' + space_group + '_' + prefix +            \
            '_fa.ins">SHELXD input file</a> - ')
    if os.path.isfile(space_group + '_' + str(prefix) + '_shelxd.log'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            + '_shelxd.log">' + 'SHELXD log file</a><br>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_ccallVSccweak.png'):
        html_all.append('<img src="' + space_group + '_' + str(prefix)        \
            + '_ccallVSccweak.png"><br>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_patfomVSccall.png'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            + '_patfomVSccall.png">' + 'PATFOM vs. CCall graph</a><br>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_occupancy.png'):
        html_all.append('<img src="' + space_group + '_' + str(prefix)        \
            + '_occupancy.png"><br>\n')
    html_all.append('</p>\n')

def write_html_efiles_standard(space_group, prefix):
    html_all.append('<h3>SHELXE</h3>\n')
    html_all.append('<p>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_shelxe.log'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            + '_shelxe.log">' + 'SHELXE orig. hand logfile </a> - ')
    if os.path.isfile(space_group + '_' + str(prefix) + '_shelxe_i.log'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            + '_shelxe_i.log">SHELXE inv. hand logfile </a><br>\n')
#Tady musi pribyt ten grafek z shelxe!!!
    if os.path.isfile(space_group + '_' + str(prefix) + '_contrast.png'):
        html_all.append('<img src="' + space_group + '_' + str(prefix) +      \
            '_contrast.png"><br>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_connectivity.png'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            + '_connectivity.png">Connectivity vs. cycle (link)</a><br>\n')
    # Tady bude vypis poctu postavenych atomu
    if os.path.isfile(space_group + '_' + str(prefix) + '.pdb'):
        standard_atoms = count_atoms(space_group + '_' + str(prefix) + '.pdb')
    else:
        standard_atoms = 0
    if os.path.isfile(space_group + '_' + str(prefix) + '_i.pdb'):
        standard_atoms_inverted = count_atoms(space_group + '_' +             \
            str(prefix) + '_i.pdb')
    else:
        standard_atoms_inverted = 0
    html_all.append('<b>Number of atoms built:</b> <i>original</i> - ' +      \
        str(standard_atoms) + '; <i>inverted</i> - ' +                        \
        str(standard_atoms_inverted) + '.\n')
    
    html_all.append('</p>\n')
    html_all.append('</div>\n')


def write_html_efiles_screen(space_group, prefix):
    html_all.append('<h3>SHELXE <i>(screening)</i></h3>\n')
    html_all.append('<p>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_contrast.png'):
        html_all.append('<img src="' + space_group + '_' + str(prefix)        \
            + '_contrast.png"><br>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_atoms_built.png'):
        html_all.append('<img src="' + space_group + '_' + str(prefix)        \
            + '_atoms_built.png"><br>\n')
    if os.path.isfile(space_group + '_' + str(prefix) + '_connectivity.png'):
        html_all.append('<a href="' + space_group + '_' + str(prefix)         \
            + '_connectivity.png">' + space_group + '_' + str(prefix)         \
            + '_connectivity.png</a><br>\n')
    html_all.append('</p>\n')
    html_all.append('</div>\n')
        





def write_html(prefix):
    global html_all
    html_all = []
    #Vypsat hlavicku
    for i in range(len(html_head1)):
        html_all.append(html_head1[i])
    # Individual SG lists
    for j in range(len(list)):
        write_html_cfiles(list[j], prefix)
        write_html_dfiles(list[j], prefix)
        if args.solvent_screen:
            write_html_efiles_screen(list[j], prefix)
        else:
            write_html_efiles_standard(list[j], prefix)
    for i in range(len(references)):
        html_all.append(references[i])
    html_all.append('</body>\n')
    html_all.append('</HTML>\n')
    with open('index_' + str(prefix) + '.html', "w") as file:
        file.writelines(html_all)
    del html_all[len(html_all)-2:len(html_all)]
    if args.screen_low and args.screen_high:
        print('Progress: ' + str(round((100 *progress) / (len(list) * 3       \
            * len(args.screen_high) * len(args.screen_low)))) + '%.')
    else:
        print('Progress: ' + str(round((100 *progress) / (len(list) * 3)))    \
            + '%.')


def html_cfiles_final(space_group, prefix): 
    global html_final
    html_final.append('<div class="sg">\n')
    html_final.append('<h2 id="' + str(space_group)                           \
        + '">Trial in space group ' + str(space_group) + '</h2>\n')
    html_final.append('<h3>SHELXC</h3>\n')
    html_final.append('<p>\n')
    # Input of SHELXC files ---TAdy potrebuju vypsat ty obrazky.
    if os.path.isfile(space_group + '_' + str(prefix) + '_'                   \
        + str(args.screen_low[0]) + '_' + str(args.screen_high[0])            \
        + '_shelxc.png'):
        html_final.append('<img src="' + str(space_group) + '_' + str(prefix) \
            + '_' + str(args.screen_low[0]) + '_' + str(args.screen_high[0])  \
            + '_shelxc_detail.png"> <br>\n')
    # Read the resolution from the _fa.ins file and put it to the HTML
    html_final.append('</p>\n')



def html_dfiles_final(sg, pref):
    global html_final
    ##################################################
    # CCALL vs. CCWEAK PLOT
    ccall = []
    ccweak = []
    patfom = []
    import matplotlib.pyplot as pltd
    pltd.figure(figsize=(10, 5),dpi=100)
    pltd.title(sg + ' - CCall vs. CCweak')
    pltd.xlabel('CCweak')
    pltd.ylabel('CCall')
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            with open(sg + '_' + str(pref) + '_' + str(args.screen_low[i])    \
                + '_' + str(args.screen_high[y]) +'_shelxd.log', "r") as dlog:
                lines = dlog.readlines()
            for z in range(len(lines)):
                if " Try" in lines[z]:
                    ccall.append(float(lines[z][31:36]))
                    ccweak.append(float(lines[z][38:43]))
                    patfom.append(float(lines[z][74:79]))
            pltd.scatter(ccweak, ccall, s=2, marker="s", label=str(pref)+'_'  \
                +str(args.screen_low[i])+'_'+str(args.screen_high[y]))
            ccall = []
            ccweak = []
            patfom = []
    pltd.legend(loc='upper left')
    pltd.savefig(sg + '_' + str(pref) + '_ccallVSccweak_all.png')
    pltd.close()
    ##################################################
    # CCALL vs. PATFOM
    ccall = []
    ccweak = []
    patfom = []
    import matplotlib.pyplot as pltd2
    pltd2.figure(figsize=(10, 5),dpi=100)
    pltd2.title(sg + ' - CCall vs. CCweak')
    pltd2.xlabel('CCweak')
    pltd2.ylabel('CCall')
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            with open(sg + '_' + str(pref) + '_' + str(args.screen_low[i])    \
                + '_' + str(args.screen_high[y]) +'_shelxd.log', "r") as dlog:
                lines = dlog.readlines()
            for z in range(len(lines)):
                if " Try" in lines[z]:
                    ccall.append(float(lines[z][31:36]))
                    ccweak.append(float(lines[z][38:43]))
                    patfom.append(float(lines[z][74:79]))
            pltd2.scatter(patfom, ccall, s=2, marker="s", label=str(pref)+'_' \
                +str(args.screen_low[i])+'_'+str(args.screen_high[y]))
            ccall = []
            ccweak = []
            patfom = []
    pltd2.legend(loc='upper left')
    pltd2.savefig(sg + '_' + str(pref) + '_ccallVSpatfom_all.png')
    pltd2.close()
    ######################################################
    # GRAPH OF OCCUPANCIES
    occup = []
    siteNo = 1
    site = []
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,5), dpi=100)
    plt.ylim(top=1)
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            occup = []
            siteNo = 1
            site = []
            with open(sg + '_' + str(pref) + '_' + str(args.screen_low[i])    \
                + '_' + str(args.screen_high[y]) +'_fa.pdb', "r") as dpdb:
                lines = dpdb.readlines()
        
            for z in range(len(lines)):
                if "HETATM" in lines[z]:
                    occup.append(float(lines[z][55:59]))
                    site.append(siteNo)
                    siteNo += 1
            plt.plot(site,occup, label=str(pref)+'_'+str(args.screen_low[i])  \
                +'_'+str(args.screen_high[y]))
    plt.title(sg + '_' + str(pref))
    plt.ylabel('Occupancy')
    plt.xlabel('Sites')
    plt.legend(loc='upper right')
    plt.savefig(sg + '_' + str(pref) + '_occupancy_all.png')
    plt.close()
    ##############################
    # INCLUDING GRAPHS TO THE HTML
    html_final.append('<h3>SHELXD</h3>\n')
    html_final.append('<p>\n')
    html_final.append('<img src="' + str(sg) + '_' + str(pref)                \
        + '_ccallVSccweak_all.png"><br>\n')
    html_final.append('<a href="' + sg + '_' + str(pref)                      \
        + '_ccallVSpatfom_all.png">' + sg + '_' + str(pref)                   \
        + '_ccallVSpatfom_all.png</a><br>\n')
    html_final.append('<img src="' + str(sg) + '_' + str(pref)                \
        + '_occupancy_all.png">\n')
    html_final.append('</p>\n')





#################################################
# GET CONTRAST, GET CONNECTIVITY FUNCTIONS
#################################################


def get_contrast(soubor):
    contrast = 0
    with open(soubor) as file:
        lines = file.readlines()
    for i in range(len(lines)):
        if "<wt>" in lines[i] and "Contrast" in lines[i]:
            contrast = float(lines[i][26:31])
    return contrast

def get_connectivity(soubor):
    connectivity = 0
    with open(soubor) as file:
        lines = file.readlines()
    for i in range(len(lines)):
        if "<wt>" in lines[i] and "Contrast" in lines[i]:
            connectivity = float(lines[i][44:49])
    return connectivity




def html_efiles_screen_final(space_group, prefix): #XXX
    html_final.append('<h3>SHELXE</h3>\n')
    html_final.append('<p>')
    ############################################################
    # INCLUDING GRAPHS TO THE HTML - 
    solv = []
    i = 0
    actual_solvent = args.solvent_screen[0]
    while actual_solvent <= args.solvent_screen[1]:
        solv.append(actual_solvent)
        actual_solvent = actual_solvent + args.solvent_screen[2]
        i = i + 1
    ##############################################################
    # INCLUDING GRAPH OF CONTRAST
    import matplotlib.pyplot as plt 
    plt.figure(figsize=(10, 5),dpi=100)
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            contrast_original = []
            contrast_inverted = []
            for z in range(len(solv)):
                contrast_original.append(get_contrast(space_group + '_'       \
                    + str(prefix) + '_' + str(args.screen_low[i]) + '_'       \
                    + str(args.screen_high[y]) + '_shelxe_0.'                 \
                    + str(solv[z]) + '.log'))
                contrast_inverted.append(get_contrast(space_group + '_'       \
                    + str(prefix) + '_' + str(args.screen_low[i]) + '_'       \
                    + str(args.screen_high[y]) + '_shelxe_0.'                 \
                    + str(solv[z]) + '_i.log'))
            plt.plot(solv, contrast_original, label=str(args.screen_low[i])   \
                +'_'+str(args.screen_high[y])+'_orig')
            plt.plot(solv, contrast_inverted, label=str(args.screen_low[i])   \
                +'_'+str(args.screen_high[y])+'_inv')
    plt.ylim([0,1])
    plt.xlim([0,100])
    plt.ylabel('Contrast')
    plt.xlabel('Solvent content')
    plt.title(space_group + ' - Solvent content vs. Contrast')
    plt.legend(loc="upper left")
    plt.savefig(space_group + '_' + str(prefix) + '_contrast_all.png')
    plt.close()
    html_final.append('<img src="' + space_group + '_' + str(prefix)          \
        + '_contrast_all.png"><br>\n')

    ##############################################################
    # INCLUDING GRAPH OF CONNECTIVITY
    import matplotlib.pyplot as plt 
    plt.figure(figsize=(10, 5),dpi=100)
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            connectivity_original = []
            connectivity_inverted = []
            for z in range(len(solv)):
                connectivity_original.append(get_connectivity(space_group     \
                    + '_' + str(prefix) + '_' + str(args.screen_low[i]) + '_' \
                    + str(args.screen_high[y]) + '_shelxe_0.' + str(solv[z])  \
                    + '.log'))
                connectivity_inverted.append(get_connectivity(space_group     \
                    + '_' + str(prefix) + '_' + str(args.screen_low[i])       \
                    + '_' + str(args.screen_high[y]) + '_shelxe_0.'           \
                    + str(solv[z]) + '_i.log'))
            plt.plot(solv, connectivity_original,                             \
                label=str(args.screen_low[i])+'_'+str(args.screen_high[y])    \
                +'_orig')
            plt.plot(solv, connectivity_inverted,                             \
                label=str(args.screen_low[i])+'_'+str(args.screen_high[y])    \
                +'_inv')
    plt.ylim([0,1])
    plt.xlim([0,100])
    plt.ylabel('Connectivity')
    plt.xlabel('Solvent content')
    plt.title(space_group + ' - Solvent content vs. Connectivity')
    plt.legend(loc="upper left")
    plt.savefig(space_group + '_' + str(prefix) + '_connectivity_all.png')
    plt.close()
    html_final.append('<a href="' + space_group + '_' + str(prefix)           \
        + '_contrast_all.png">' + space_group + '_' + str(prefix)             \
        + '_contrast_all.png</a><br>\n')
    
    ##############################################################
    # INCLUDING GRAPH OF ATOMS BUILT
    import matplotlib.pyplot as plt 
    plt.figure(figsize=(10, 5),dpi=100)
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            screening_atoms_original = []
            screening_atoms_inverted = []
            for z in range(len(solv)):
                # Test if file exists
                if os.path.isfile(space_group + '_' + str(prefix) + '_'       \
                    + str(args.screen_low[i]) + '_' + str(args.screen_high[y])\
                    + '_' + str(solv[z]) + '.pdb'):
                    screening_atoms_original.append(count_atoms(space_group   \
                        + '_' + str(prefix) + '_' + str(args.screen_low[i])   \
                        + '_' + str(args.screen_high[y]) + '_' + str(solv[z]) \
                        + '.pdb'))
                else:
                    # When file does not exist
                    screening_atoms_original.append(0)
                # Test if file exists
                if os.path.isfile(space_group + '_' + str(prefix) + '_'       \
                    + str(args.screen_low[i]) + '_' + str(args.screen_high[y])\
                    + '_' + str(solv[z]) + '_i.pdb'):
                    screening_atoms_inverted.append(count_atoms(space_group   \
                        + '_' + str(prefix) + '_' + str(args.screen_low[i])   \
                        + '_' + str(args.screen_high[y]) + '_' + str(solv[z]) \
                        + '_i.pdb'))
                else:
                    # When file does not exist
                    screening_atoms_inverted.append(0)
            plt.plot(solv, screening_atoms_original,                          \
                label=str(args.screen_low[i])+'_'+str(args.screen_high[y])    \
                +'_orig')
            plt.plot(solv, screening_atoms_inverted,                          \
                label=str(args.screen_low[i])+'_'+str(args.screen_high[y])    \
                +'_inv')
    plt.ylim(bottom=0)
    plt.xlim([0,100])
    plt.ylabel('Atoms built')
    plt.xlabel('Solvent content')
    plt.title(space_group + ' - Atoms built')
    plt.legend(loc="upper left")
    plt.savefig(space_group + '_' + str(prefix) + '_atoms_built_all.png')
    plt.close()
    html_final.append('<img src="' + space_group + '_' + str(prefix)          \
        + '_atoms_built_all.png"><br>\n')
    html_final.append('</p>\n')
    html_final.append('</div>\n')

def html_efiles_standard(space_group, prefix):
    global html_final
    print('Delam funkci html_efiles_standard')
    contrast_original = [0] 
    contrast_inverted = [0]
    connectivity_original = [0]
    connectivity_inverted = [0]
    cycle = [0]
    import matplotlib.pyplot as plt1
    plt1.figure(figsize=(10,5),dpi=100)
    plt1.ylim(top=1)
    plt1.title(space_group + ' - Contrast vs. cycle')
    plt1.ylabel('Contrast')
    plt1.xlabel('Cycle')
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            contrast_original = [0] 
            contrast_inverted = [0]
            cycle = [0]
            with open(space_group + '_' + str(prefix) + '_'                   \
                + str(args.screen_low[i]) + '_' + str(args.screen_high[y])    \
                + '_shelxe.log') as file:
                lines = file.readlines()
            a = 1
            for j in range(len(lines)):
                if "<wt>" in lines[j] and "Contrast" in lines[j]:
                    contrast_original.append(float(lines[j][26:31]))
                    cycle.append(a)
                    a = a + 1
            with open(space_group + '_' + str(prefix) + '_'                   \
                + str(args.screen_low[i]) + '_' + str(args.screen_high[y])    \
                + '_shelxe_i.log') as file:
                lines = file.readlines()
            a = 1
            for j in range(len(lines)):
                if "<wt>" in lines[j] and "Contrast" in lines[j]:
                    contrast_inverted.append(float(lines[j][26:31]))
                    connectivity_inverted.append(float(lines[j][26:31]))
                    #cycle.append(a)
                    a = a + 1
            plt1.plot(cycle, contrast_original, label=str(args.screen_low[i]) \
                +'_'+str(args.screen_high[y])+'_orig')
            plt1.plot(cycle, contrast_inverted, label=str(args.screen_low[i]) \
                +'_'+str(args.screen_high[y])+'_inv')
    plt1.legend()
    plt1.savefig(space_group + '_' + str(prefix) + '_contrast_all.png')
# Connectivity
    import matplotlib.pyplot as plt2
    plt2.figure(figsize=(10,5),dpi=100)
    plt2.ylim(top=1)
    plt2.title(space_group + ' - Connectivity vs. cycle')
    plt2.ylabel('Connectivity')
    plt2.xlabel('Cycle')
    #plt1.legend(loc="upper left")
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            connectivity_original = [0]
            connectivity_inverted = [0]
            cycle = [0]
            with open(space_group + '_' + str(prefix) + '_'                   \
                + str(args.screen_low[i]) + '_' + str(args.screen_high[y])    \
                + '_shelxe.log') as file:
                lines = file.readlines()
            a = 1
            for j in range(len(lines)):
                if "<wt>" in lines[j] and "Contrast" in lines[j]:
                    connectivity_original.append(float(lines[j][44:49]))
                    cycle.append(a)
                    a = a + 1
            with open(space_group + '_' + str(prefix) + '_'                   \
                + str(args.screen_low[i]) + '_' + str(args.screen_high[y])    \
                + '_shelxe_i.log') as file:
                lines = file.readlines()
            a = 1
            for j in range(len(lines)):
                if "<wt>" in lines[j] and "Contrast" in lines[j]:
                    connectivity_inverted.append(float(lines[j][44:49]))
                    #cycle.append(a)
                    a = a + 1
            plt1.plot(cycle, connectivity_original,                           \
                label=str(args.screen_low[i])+'_'+str(args.screen_high[y])    \
                +'_orig')
            plt1.plot(cycle, connectivity_inverted,                           \
                label=str(args.screen_low[i])+'_'+str(args.screen_high[y])    \
                +'_inv')
    plt2.legend()
    plt2.savefig(space_group + '_' + str(prefix) + '_connectivity_all.png')
    ##################################################
    # MAKING LINKS TO THE HTML
    html_final.append('<h3>SHELXE</h3>\n')
    html_final.append('<p>\n')
    html_final.append('<img src="' + space_group + '_' + str(prefix)          \
        + '_contrast_all.png"><br>\n')
    html_final.append('<img src="' + space_group + '_' + str(prefix)          \
        + '_connectivity_all.png">\n')
    html_final.append('</p>\n')






def write_html_screen(prefix):
    global html_final
    html_final = []
    html_head1[18] = ''
    html_head1[25] = '<tr><td>Status:</td><td>finished</td></tr>\n'
    for i in range(len(html_head1)):
        html_final.append(html_head1[i])
    html_final.append('<h2>Links to the individual runs:</h2>\n')
    html_final.append('<p>\n')
    for i in range(len(args.screen_low)):
        for y in range(len(args.screen_high)):
            html_final.append('<a href="index_' + prefix + '_'                \
                + str(args.screen_low[i]) + '_' + str(args.screen_high[y])    \
                + '.html">' + prefix + '_' + str(args.screen_low[i]) + '_'    \
                + str(args.screen_high[y]) + '.html</a><br>\n')
    html_final.append('</p>\n')
    for j in range(len(list)):
        html_cfiles_final(list[j], prefix)
        html_dfiles_final(list[j], prefix)
        if args.solvent_screen:
            html_efiles_screen_final(list[j], prefix)
        else:
            html_efiles_standard(list[j], prefix)

#'<h2>References</h2>\n', '<p>\n',
#        'P. Kolenko, J. Stransky, T. Koval, M. Maly, J. Dohnalek. (2021).'    \
#        + ' SHELIXIR: automation of experimental phasing procedures using'    \
#        + ' SHELXC/D/E. <i>J. Appl. Cryst.</i>, <b>54</b>,'                   \
#        + ' https://doi.org/10.1107/S1600576721002454.\n', '</p>\n',
#        '<p>\n', 'Please cite: I. Uson & G.M. Sheldrick (2018),'              \
#        + ' An introduction to experimental phasing of macromolecules'        \
#        + ' illustrated by SHELX; new autotracing features" Acta Cryst. D74,' \
#        + ' 106-116 (Open Access) if SHELXE proves useful.\n', '</p>\n',

    for i in range(len(references)):
        html_final.append(references[i])        
    html_final.append('</body>\n')
    html_final.append('</HTML>\n')
    with open('index.html', "w") as file:
        file.writelines(html_final)
    print('Final HTML produced: index.html')






##################################################
# SHELX C CYCLE
##################################################

def run_c(space_group, prefix):
    global progress
    print('Running SHELXC in ' + space_group + '.')
    c_file[1] = 'SPAG ' + space_group
    with open(space_group + '_' + str(prefix) + '_shelxc.inp', mode='wt',     \
        encoding='utf-8') as myfile:
        myfile.write('\n'.join(c_file))
    os.system('shelxc ' + space_group + '_' + prefix + ' < ' + space_group +  \
        '_' + str(prefix) + '_shelxc.inp > ' + space_group + '_' + str(prefix)\
        + '_shelxc.log')
    progress += 1




###################################################
## CREATING SHELX C GRAPHS
################################################### 

def c_graph(space_group, prefix):
    input_array = []
    readme = open(space_group + '_' + str(prefix) +                           \
    	'_shelxc.log', 'r').readlines()
    before = False
    #for all defined anomalous data do...
    for file_type in list_of_files: 
        name_array = file_type + "_array" 
    # create a list of them and store the anomalous signal
        vars()[name_array] = []  
        name_res = file_type + "_res" 
    # store the resolution at which the anomalous differences are calculated
        vars()[name_res] = []
        for i in range(len(readme)):
            if ("from " in readme[i] and file_type in readme[i] and " file"   \
                in readme[i]):
                input_array.append(file_type)
                before = True
            if ('Resl. ' in readme[i] and before):
                for k in range(len(readme[i].split()) -2):
                    vars()[name_res].append(float(readme[i].split()[k+2]))
            if ('<d"/' in readme[i] and before):
                for j in range(len(readme[i].split()) - 1):
                    vars()[name_array].append(float(readme[i].split()[j+1]))
                before = False
# Here starts the plot for SHELXC procedure    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5),dpi=100)
    for file_type in list_of_files:
        # create a list of them and store the anomalous signal
        name_array = file_type + "_array"
        # store the resolution at which the anomalous differences are calc.
        name_res = file_type + "_res"
        plt.plot(vars()[name_res], vars()[name_array], label=file_type)
    plt.legend(loc="upper left")
    plt.ylabel('<d"/sig>')
    plt.xlabel('Resolution')
    plt.title(space_group + ' - <d"/sig> vs. Resolution')
    plt.axhline(y=1, color='g', linestyle='-.')
    plt.savefig(space_group + '_' + str(prefix) + '_shelxc.png')
    plt.xlim(right=5)
    plt.savefig(space_group + '_' + str(prefix) + '_shelxc_detail.png')
    plt.close()


##################################################
# RUNNING SHELX D
################################################## 

def d_res(space_group, prefix, a, b):
    with open(space_group + '_' + str(prefix) + '_fa.ins', "r") as file:
        lines = file.readlines()
    for i in range(len(lines)):
        if lines[i][0:4] == "SHEL":
            lines[i] = 'SHEL ' + str(a) + ' ' + str(b) + '\n'
    #file.writelines(lines)
    with open(space_group + '_' + str(prefix) + '_fa.ins', "w") as fajl:
        fajl.writelines(lines)

def d_best(space_group, prefix):
    with open(space_group + '_' + str(prefix) + '_shelxd.log', "r") as file:
        lines = file.readlines()
    print('The best CFOM: ' + lines[-5][60:65] + '.')
    best = float(lines[-5][60:65])

def get_CFOM(space_group, prefix):
    with open(space_group + '_' + str(prefix) + '_shelxd.log', "r") as file:
        lines = file.readlines()
    return float(lines[-5][60:65])

def run_d(space_group, prefix):
    global progress
    print('Running SHELXD in ' + space_group + '.')
    os.system('shelxd ' + space_group + '_' + str(prefix) \
        + '_fa > ' + space_group + '_' + str(prefix) + '_shelxd.log')
    progress += 1
#    d_best(str(space_group), str(prefix))


##################################################
# SHELXD GRAPHS
##################################################

def d_graph(space_group, prefix):
##################################################
# DEFINITION OF CCALL, CCWEAK AND PATFOM FOR GRAPHS 
    ccall = []
    ccweak = []
    patfom = []
##################################################
# READING OF D LOGFINE
    with open(space_group + '_' + str(prefix) + '_shelxd.log', "r") as dlog:
        lines = dlog.readlines()
    for i in range(len(lines)):
        if " Try" in lines[i]:
            # Extracts CCall from the SHELXD output
            ccall.append(float(lines[i][31:36]))
            # Extracts CCweak from the SHELXD output
            ccweak.append(float(lines[i][38:43]))
            # Extracts PATFOM from the SHELXD output
            patfom.append(float(lines[i][74:79]))


##################################################
# PLOTTING GRAPHS OF SHELX D
    import matplotlib.pyplot as pltd
    pltd.figure(figsize=(10, 5),dpi=100)
    pltd.scatter(ccweak, ccall, s=10)
    pltd.title(space_group + ' - CCall vs. CCweak')
    pltd.xlabel('CCweak')
    pltd.ylabel('CCall')
    pltd.savefig(space_group + '_' + str(prefix) + '_ccallVSccweak.png')
    pltd.close()
    import matplotlib.pyplot as pltd
    pltd.figure(figsize=(10, 5),dpi=100)
    pltd.scatter(patfom, ccall, s=10)
    pltd.title(space_group + ' - PATFOM vs. CCall')
    pltd.xlabel('CCall')
    pltd.ylabel('PATFOM')
    pltd.savefig(space_group + '_' + str(prefix) + '_patfomVSccall.png')
    pltd.close()
##################################################
# Site occupancy vs site number graph
#reads fa.pdb for number of occupancies
    with open(space_group + '_' + str(prefix) + '_fa.pdb', "r") as dpdb: 
        lines = dpdb.readlines()
    occup = []
    siteNo = 1
    site = []
    
# reads PDB file for heavy elements
    for i in range(len(lines)):                     
        if "HETATM" in lines[i]:
            # appends occupancy to the matrix
            occup.append(float(lines[i][55:59]))    
            # appends number of element
            site.append(siteNo)                     
            siteNo += 1
    
# Create graph of sites
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5),dpi=100)
    plt.ylim(top=1)
    plt.plot(site, occup)
    plt.title(space_group + ' - Site occupancy vs. site number')
    plt.ylabel('Occupancy')
    plt.xlabel('Sites')
    plt.savefig(space_group + '_' + str(prefix) + '_occupancy.png')
    plt.close()




##################################################
# STANDARD SHELXE
##################################################

def count_atoms(file):
    number_of_atoms = 0
    with open(file) as fajl:
        lines = fajl.readlines()
    for i in range(len(lines)):
        if "ATOM" in lines[i]:
            number_of_atoms = number_of_atoms + 1
    return(number_of_atoms)


def run_e_parallel(process):
    #os.system('shelxe {}'.format(process))
    os.system(bine + ' {}'.format(process))

def e_standard_matrices(space_group, prefix):
    work_contrast_original = [0]
    work_contrast_inverted = [0]
    work_connectivity_original = [0]
    work_connectivity_inverted = [0]
    cycle = [0]
##################################################
# READING ORIGINAL CONTRAST AND CONNECTIVITY
    with open(space_group + '_' + str(prefix) + '_shelxe.log') as file:
        lines = file.readlines()
    a = 1
    for j in range(len(lines)):
        if "<wt>" in lines[j] and "Contrast" in lines[j]:
            work_contrast_original.append(float(lines[j][26:31]))
            work_connectivity_original.append(float(lines[j][44:49]))
            cycle.append(a)
            a = a + 1
##################################################
# READING INVERTED CONTRAST AND CONNECTIVITY
    with open(space_group + '_' + str(prefix) + '_shelxe_i.log') as file:
        lines = file.readlines()
    a = 1
    for j in range(len(lines)):
        if "<wt>" in lines[j] and "Contrast" in lines[j]:
            work_contrast_inverted.append(float(lines[j][26:31]))
            work_connectivity_inverted.append(float(lines[j][44:49]))
            a = a + 1
##################################################
# MAKING PLOT
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5),dpi=100)
    plt.ylim(top=1)
    plt.plot(cycle, work_contrast_original)
    plt.plot(cycle, work_contrast_inverted)
    plt.title(space_group + ' - Contrast vs. cycle')
    plt.ylabel('Contrast')
    plt.xlabel('Cycle')
    plt.legend(('Original', 'Inverted'), loc="upper left")
    plt.savefig(space_group + '_' + str(prefix) + '_contrast.png')
    plt.close()
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5),dpi=100)
    plt.ylim(top=1)
    plt.plot(cycle, work_connectivity_original)
    plt.plot(cycle, work_connectivity_inverted)
    plt.title(space_group + ' - Connectivity vs. cycle')
    plt.ylabel('Connectivity')
    plt.xlabel('Cycle')
    plt.legend(('Original', 'Inverted'), loc="upper left")
    plt.savefig(space_group + '_' + str(prefix) + '_connectivity.png')
    plt.close()
    
        



def run_e_standard(space_group, prefix):
    global progress
    print('Running SHELXE in ' + space_group + '.   ...standard')
    processes = []
    processes.append(space_group + '_' + str(prefix) + ' ' + space_group      \
        + '_' + str(prefix) + '_fa ' + str(args.SHELXE_parameters)            \
        + ' > ' + space_group + '_' + str(prefix) +  '_shelxe.log')
    processes.append(space_group + '_' + str(prefix) + ' ' + space_group      \
        + '_' + str(prefix) + '_fa ' + str(args.SHELXE_parameters) +          \
        ' -i > ' + space_group + '_' + str(prefix) + '_shelxe_i.log')
    pool = mp.Pool(processes = args.nproc)
    pool.map(run_e_parallel, processes)
    ##################################################
    # PREPARING OUTPUT
    if os.path.isfile(space_group + '_' + str(prefix) + '.pdb'):
        standard_atoms[0] = count_atoms(space_group + '_' + str(prefix)       \
            + '.pdb')
    else:
        standard_atoms[0] = 0
    if os.path.isfile(space_group + '_' + str(prefix) + '_i.pdb'):
        standard_atoms[1] = count_atoms(space_group + '_' + str(prefix)       \
            + '_i.pdb')
    else:
        standard_atoms[1] = 0
    progress += 1


##################################################
# SCREENING SHELXE
##################################################

def e_screen_matrices(sg, prefix):
    actual_solvent = args.solvent_screen[0]
    i = 0
    while actual_solvent <= args.solvent_screen[1]:
# Counting atoms original and inverted
        if os.path.isfile(sg + '_' + str(prefix) + '_' + str(actual_solvent)  \
            + '.pdb'):
            screening_atoms_original[i] = count_atoms(sg + '_' + str(prefix)  \
                + '_' + str(actual_solvent) + '.pdb')
        else:
            screening_atoms_original[i] = 0
        if os.path.isfile(sg + '_' + str(prefix) + '_' + str(actual_solvent)  \
            + '_' + str(actual_solvent) + '_i.pdb'):
            screening_atoms_inverted[i] = count_atoms(sg + '_' + str(prefix)  \
                + '_' + str(actual_solvent) + '_i.pdb')
        else:
            screening_atoms_inverted[i] = 0
# reading original contrast
        with open(sg + '_' + str(prefix) + '_shelxe_0.' + str(actual_solvent) \
            + '.log', "r") as file:
            lines = file.readlines()
        for j in range(len(lines)):
            if "<wt>" in lines[j] and "Contrast" in lines[j]:
                work_contrast = lines[j][26:31]
                work_connectivity = lines[j][44:49]
        screening_contrast_original[i] = float(work_contrast)
        screening_connectivity_original[i] = float(work_connectivity)
# reading inverted contrast
        with open(sg + '_' + str(prefix) + '_shelxe_0.' + str(actual_solvent) \
            + '_i.log', "r") as file:
            lines = file.readlines()
        for k in range(len(lines)):
            if "<wt>" in lines[k] and "Contrast" in lines[k]:
                work_contrast = lines[k][26:31]
                work_connectivity = lines[k][44:49]
        screening_contrast_inverted[i] = float(work_contrast)
        screening_connectivity_inverted[i] = float(work_connectivity)
# finalizing the loop
        actual_solvent = actual_solvent + args.solvent_screen[2]
        i = i + 1



##################################################
# GRAPH_E_SCREEN
def graph_e_screen(sg, prefix):
    solv = []
    i = 0
    actual_solvent = args.solvent_screen[0]
    while actual_solvent <= args.solvent_screen[1]:
        solv.append(actual_solvent)
        actual_solvent = actual_solvent + args.solvent_screen[2]
        i = i + 1
    import matplotlib.pyplot as plt                # Graph of atoms built
    plt.figure(figsize=(10, 5),dpi=100)
    plt.plot(solv, screening_atoms_original)
    plt.plot(solv, screening_atoms_inverted)
    plt.ylim(bottom=0)
    plt.ylabel('Atoms built')
    plt.xlabel('Solvent content')
    plt.title(sg + ' - Atoms built')
    plt.legend(('Original', 'Inverted'), loc="upper left")
    plt.savefig(sg + '_' + str(prefix) + '_atoms_built.png')
    plt.close()
    import matplotlib.pyplot as plt                # Graph of contrast
    plt.figure(figsize=(10, 5),dpi=100)
    plt.plot(solv, screening_contrast_original)
    plt.plot(solv, screening_contrast_inverted)
    plt.ylim(bottom=0, top=1)
    plt.ylabel('Contrast')
    plt.xlabel('Solvent content')
    plt.title(sg + ' - Contrast vs. solvent content')
    plt.legend(('Original', 'Inverted'), loc="upper left")
    plt.savefig(sg + '_' + str(prefix) + '_contrast.png')
    plt.close()
    import matplotlib.pyplot as plt                # Graph of connectivity
    plt.figure(figsize=(10, 5),dpi=100)
    plt.plot(solv, screening_connectivity_original)
    plt.plot(solv, screening_connectivity_inverted)
    plt.ylim(bottom=0, top=1)
    plt.ylabel('Connectivity')
    plt.xlabel('Solvent content')
    plt.title(sg + ' - Connectivity vs. solvent content')
    plt.legend(('Original', 'Inverted'), loc="upper left")
    plt.savefig(sg + '_' + str(prefix) + '_connectivity.png')
    plt.close()
    solv = []
    

def run_e_screen(space_group, prefix):
    global progress
    print('Running SHELXE in ' + space_group + '.    ...screening')
    # initialize of parallelization
    processes = []
    # setting of initial actual solvent
    actual_solvent = args.solvent_screen[0]
    # initialize list of solvents to be tested
    while actual_solvent <= args.solvent_screen[1]:
        #print('current solvent is: ' + str(actual_solvent))
        os.symlink(space_group + '_' + str(prefix) + '.hkl',                  \
            space_group + '_' + str(prefix) + '_' + str(actual_solvent)       \
            + '.hkl')

# appending direct hand processes
        processes.append(space_group + '_' + str(prefix) + '_'                \
            + str(actual_solvent) + ' ' + space_group + '_' + str(prefix)     \
            + '_fa ' + str(args.SHELXE_parameters) + ' -s0.'                  \
            + str(actual_solvent) + ' > ' + space_group +  '_' + str(prefix)  \
            + '_shelxe_0.' + str(actual_solvent) + '.log')
# appending iverted hand processes
        processes.append(space_group + '_' + str(prefix) + '_'                \
            + str(actual_solvent) + ' ' + space_group + '_' + str(prefix)     \
            + '_fa ' + str(args.SHELXE_parameters) + ' -s0.'                  \
            + str(actual_solvent) + ' -i > ' + space_group + '_' + str(prefix)\
            + '_shelxe_0.' + str(actual_solvent) + '_i.log')
        actual_solvent = actual_solvent + args.solvent_screen[2]
##################################################
# Creation and execution of pool
    pool = mp.Pool(processes = args.nproc)
    pool.map(run_e_parallel, processes)
    # Returns the actual solvent to start for another space groups
    actual_solvent = args.solvent_screen[0]
    progress += 1





##################################################
# GLOBAL FUNCTION DEFINITION
##################################################

def global_function(prefix):
    read_hkl_file()
    html_init()
    c_file_append()
    sg_list_generation()
    for sg in list:
        run_c(sg, prefix)
        write_html(prefix)
        c_graph(sg, prefix)
        if args.res:
            d_res(sg, prefix, args.res[0], args.res[1])
        run_d(sg, prefix)
        d_graph(sg, prefix)
        write_html(prefix)
        if args.CFOM_cutoff:
            if get_CFOM(sg, prefix) >= args.CFOM_cutoff:
                if args.solvent_screen:
                    run_e_screen(sg, prefix)
                    e_screen_matrices(sg, prefix)
                    graph_e_screen(sg, prefix)
                else:
                    run_e_standard(sg, prefix)
                    e_standard_matrices(sg, prefix)
            else:
                print('Solution in space group ' + sg + ' has low potential.' \
                    + 'Skipping ...')
        else:
            if args.solvent_screen:
                run_e_screen(sg, prefix)
                e_screen_matrices(sg, prefix)
                graph_e_screen(sg, prefix)
            else:
                run_e_standard(sg, prefix)
                e_standard_matrices(sg, prefix)
    html_head1[18] = ''
    html_head1[25] = '<tr><td>Status:</td><td>finished</td></tr>\n'
    write_html(prefix)

##################################################
# GLOBAL SCREEN FUNCTION
##################################################

def global_screen(prefix, a, b):
    html_init()
    sg_list_generation()
    for sg in list:
        run_c(sg, prefix)
        c_graph(sg, prefix)
        write_html(prefix)
        if args.screen_low and args.screen_high:
            d_res(sg, prefix, a, b)
        run_d(sg, prefix)
        d_graph(sg, prefix)
        write_html(prefix)
        if args.CFOM_cutoff:
            if get_CFOM(sg, prefix) >= args.CFOM_cutoff:
                if args.solvent_screen:
                    run_e_screen(sg, prefix)
                    e_screen_matrices(sg, prefix)
                    graph_e_screen(sg, prefix)
                else:
                    run_e_standard(sg, prefix)
                    e_standard_matrices(sg, prefix)
            else:
                print('Solution in space group ' + sg + ' has low potential.' \
                    + 'Skipping ...')
        else:
            if args.solvent_screen:
                run_e_screen(sg, prefix)
                e_screen_matrices(sg, prefix)
                graph_e_screen(sg, prefix)
            else:
                run_e_standard(sg, prefix)
                e_standard_matrices(sg, prefix)
        write_html(prefix)
    html_head1[18] = ''
    html_head1[25] = '<tr><td>Status:</td><td>finished</td></tr>\n'
    write_html(prefix)




##################################################
# SHELXE MR STANDARD ALGORITHM
##################################################

def mr_shelxe_standard():
    print('SHELXE fragment extension.')
    os.symlink(args.sequence_file, 'mr-' + args.prefix + '.seq')
    os.system(bine + ' mr-' + args.prefix + '.pda ' + args.SHELXE_parameters  \
        + ' > mr-' + args.prefix + '_shelxe.log')
##################################################
# READING ORIGINAL CONTRAST AND CONNECTIVITY
    contrast = []
    connectivity = []
    cycle = []
    with open('mr-' + str(args.prefix) + '_shelxe.log') as file:
        lines = file.readlines()
    a = 1
    for j in range(len(lines)):
        if "<wt>" in lines[j] and "Contrast" in lines[j]:
            contrast.append(float(lines[j][26:31]))
            connectivity.append(float(lines[j][44:49]))
            cycle.append(a)
            a = a + 1
##################################################
# MAKING PLOT
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5),dpi=100)
    plt.ylim(top=1)
    plt.plot(cycle, contrast)
    plt.title(args.prefix + ' - Contrast vs. cycle')
    plt.ylabel('Contrast')
    plt.xlabel('Cycle')
    plt.savefig(str(args.prefix) + '_contrast.png')
    plt.close()
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5),dpi=100)
    plt.ylim(top=1)
    plt.plot(cycle, connectivity)
    plt.title(str(args.prefix) + ' - Connectivity vs. cycle')
    plt.ylabel('Connectivity')
    plt.xlabel('Cycle')
    plt.savefig(str(args.prefix) + '_connectivity.png')
    plt.close()
##################################################
# MAKING HTML
    html_file = ['<HTML>\n', '<head>\n', '<meta charset="utf-8">\n', 
        '<title>Project</title>\n', '</head>\n', '<body>\n',
        '<h1 align="center"><i>SHELIXIR</i> - ' + args.prefix + '</h1>\n',
        '<h2>Input files</h2>\n', '<p>\n',
        'Input data: ' + str(args.nat) + '<br>\n',
        'Input model: ' + str(args.molecular_replacement) + '</p>\n',
        '<h2>Results</h2>\n', '<p>\n', 'Log file: <a href="mr-' + args.prefix \
            + '_shelxe.log">mr-' + args.prefix + '_shelxe.log</a>\n', '</p>\n',
        '<img src="' + str(args.prefix) + '_contrast.png">\n', 
        '<img src="' + str(args.prefix) + '_connectivity.png">\n',
        '<p>Atoms in: ' + str(count_atoms(args.molecular_replacement))        \
            + '<br>\n',
        'Atoms out: ' + str(count_atoms('mr-' + str(args.prefix)              \
            + '.pdb')) + '</p>\n', '<h2>References</h2>\n', '<p>\n',
        'P. Kolenko, J. Stransky, T. Koval, M. Maly, J. Dohnalek. (2021).'    \
        + ' SHELIXIR: automation of experimental phasing procedures using'    \
        + ' SHELXC/D/E. <i>J. Appl. Cryst.</i>, <b>54</b>,'                   \
        + ' https://doi.org/10.1107/S1600576721002454.\n', '</p>\n',
        '<p>\n', 'Please cite: I. Uson & G.M. Sheldrick (2018),'              \
        + ' An introduction to experimental phasing of macromolecules'        \
        + ' illustrated by SHELX; new autotracing features" Acta Cryst. D74,' \
        + ' 106-116 (Open Access) if SHELXE proves useful.\n', '</p>\n',
        '</body>\n', '</HTML>\n'] 
    with open('index.html', "w") as file:
        file.writelines(html_file)
    print('Final HTML produced: index.html')

##################################################
# SHELXE MR SCREENING ALGORITHM
##################################################

def mr_shelxe_screening():
    print('SHELXE fragment extension - solvent screening.')
    # initialize of parallelization
    processes = []
    # setting of initial actual solvent
    actual_solvent = args.solvent_screen[0]
    # initialize list of solvents to be tested
    while actual_solvent <= args.solvent_screen[1]:
        os.symlink('mr-' + args.prefix + '.hkl', 'mr-' + args.prefix + '_0.'  \
            + str(actual_solvent) + '.hkl')
        os.symlink('mr-' + args.prefix + '.pda', 'mr-' + args.prefix + '_0.'  \
            + str(actual_solvent) + '.pda')
        if args.sequence_file:
            os.symlink(args.sequence_file, 'mr-' + args.prefix + '_0.'        \
                + str(actual_solvent) + '.seq')
# appending processes
        processes.append('mr-' + args.prefix + '_0.' + str(actual_solvent)    \
            + '.pda ' + str(args.SHELXE_parameters) + ' -s0.'                 \
            + str(actual_solvent) + ' > mr-' + str(args.prefix) + '_shelxe_0.'\
            + str(actual_solvent) + '.log')
        actual_solvent = actual_solvent + args.solvent_screen[2]
##################################################
# Creation and execution of pool
    pool = mp.Pool(processes = args.nproc)
    pool.map(run_e_parallel, processes)
#XXX
##################################################
# Generation of matrices
    actual_solvent = args.solvent_screen[0]
    i = 0
    contrast = []
    connectivity = []
    solv = []
    atoms = []
    while actual_solvent <= args.solvent_screen[1]:
# Counting atoms original and inverted
        atoms.append(count_atoms('mr-' + args.prefix + '_0.'                  \
            + str(actual_solvent) + '.pdb'))
# reading original contrast
        with open('mr-' + args.prefix + '_shelxe_0.' + str(actual_solvent)    \
            + '.log', "r") as file:
            lines = file.readlines()
        for j in range(len(lines)):
            if "<wt>" in lines[j] and "Contrast" in lines[j]:
                work_contrast = lines[j][26:31]
                work_connectivity = lines[j][44:49]
        contrast.append(float(work_contrast))
        connectivity.append(float(work_connectivity))
# finalizing the loop
        solv.append(actual_solvent)
        actual_solvent = actual_solvent + args.solvent_screen[2]
        i = i + 1
## YYY - dodelat
    import matplotlib.pyplot as plt                # Graph of atoms built
    plt.figure(figsize=(10, 5),dpi=100)
    plt.plot(solv, atoms)
    plt.ylim(bottom=0)
    plt.ylabel('Atoms built')
    plt.xlabel('Solvent content')
    plt.title(args.prefix + ' - Atoms built')
    plt.savefig(args.prefix + '_atoms_built.png')
    plt.close()
    import matplotlib.pyplot as plt                # Graph of contrast
    plt.figure(figsize=(10, 5),dpi=100)
    plt.plot(solv, contrast)
    plt.ylim(bottom=0, top=1)
    plt.ylabel('Contrast')
    plt.xlabel('Solvent content')
    plt.title(args.prefix + ' - Contrast vs. solvent content')
    plt.savefig(args.prefix + '_contrast.png')
    plt.close()
    import matplotlib.pyplot as plt                # Graph of connectivity
    plt.figure(figsize=(10, 5),dpi=100)
    plt.plot(solv, connectivity)
    plt.ylim(bottom=0, top=1)
    plt.ylabel('Connectivity')
    plt.xlabel('Solvent content')
    plt.title(args.prefix + ' - Connectivity vs. solvent content')
    plt.savefig(args.prefix + '_connectivity.png')
    plt.close()
##################################################
# MAKING HTML
    html_file = ['<HTML>\n', '<head>\n', '<meta charset="utf-8">\n', 
        '<title>Project</title>\n', '</head>\n', '<body>\n',
        '<h1 align="center"><i>SHELIXIR</i> - ' + args.prefix + '</h1>\n',
        '<h2>Input files</h2>\n', '<p>\n',
        'Input data: ' + str(args.nat) + '<br>\n',
        'Input model: ' + str(args.molecular_replacement) + '<br>\n',
        'SHELXE parameters: ' + str(args.SHELXE_parameters) + '</p>\n',
        '<h2>Results</h2>\n', '<p>\n', 
        '<img src="' + str(args.prefix) + '_contrast.png">\n', 
        '<img src="' + str(args.prefix) + '_connectivity.png">\n',
        '<img src="' + str(args.prefix) + '_atoms_built.png">\n',
        '<h2>References</h2>\n', '<p>\n',
        'P. Kolenko, J. Stransky, T. Koval, M. Maly, J. Dohnalek. (2021).'    \
        + ' SHELIXIR: automation of experimental phasing procedures using'    \
        + ' SHELXC/D/E. <i>J. Appl. Cryst.</i>, <b>54</b>,'                   \
        + ' https://doi.org/10.1107/S1600576721002454.\n', '</p>\n',
        '<p>\n', 'Please cite: I. Uson & G.M. Sheldrick (2018),'              \
        + ' An introduction to experimental phasing of macromolecules'        \
        + ' illustrated by SHELX; new autotracing features" Acta Cryst. D74,' \
        + ' 106-116 (Open Access) if SHELXE proves useful.\n', '</p>\n',
        '</body>\n', '</HTML>\n'] 
    with open('index.html', "w") as file:
        file.writelines(html_file)
    print('Final HTML produced: index.html')    





##################################################
# SCREENING ALGORITHM
##################################################

def main():

    if args.molecular_replacement:
        if args.solvent_screen:
            mr_shelxe_screening()
        else:
            mr_shelxe_standard()
    elif args.screen_low and not args.screen_high:
        print('Please, specify the high resolution limit. Exiting ...')
    elif args.screen_high and not args.screen_low:
        args.screen_low = [999]
        print('Low resolution limit is not specified. It will be set to 999 AA.')
        read_hkl_file()
        c_file_append()
        for i in range(len(args.screen_low)):
            for y in range(len(args.screen_high)):
                work_prefix = args.prefix + '_' + str(args.screen_low[i]) + '_'   \
                    + str(args.screen_high[y])
                global_screen(work_prefix, args.screen_low[i], args.screen_high[y])
                html_head1[18] = '<meta http-equiv="refresh" content="10">'
                html_head1[25] = '<tr><td>Status:</td><td bgcolor="orange">'      \
                    + 'running ...</td></tr>\n'
        write_html_screen(args.prefix)
    
    elif args.screen_low and args.screen_high:
        read_hkl_file()
        c_file_append()
        for i in range(len(args.screen_low)):
            for y in range(len(args.screen_high)):
                work_prefix = args.prefix + '_' + str(args.screen_low[i]) + '_'   \
                    + str(args.screen_high[y])
                global_screen(work_prefix, args.screen_low[i], args.screen_high[y])
                html_head1[18] = '<meta http-equiv="refresh" content="10">'
                html_head1[25] = '<tr><td>Status:</td><td bgcolor="orange">'      \
                    + 'running ...</td></tr>\n'
        write_html_screen(args.prefix)
    else:
        global_function(args.prefix)
