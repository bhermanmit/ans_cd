#!/usr/bin/env python

from __future__ import division

import os
import csv

tracks      = {   '0': "Accelerator Applications",
                  '1': "Aerospace Nuclear Science & Technology",
                  '2': "Biology & Medicine",
                  '3': "Decommissioning, Decontamination & Reutilization",
                  '4': "Detection & Measurements",
                  '5': "Education, Training & Workforce Development",
                  '6': "Environmental Sciences",
                  '7': "Fuel Cycle & Waste Management",
                  '8': "Fusion Energy & Plasmas",
                  '9': "Human Factors, Instrumentation & Controls",
                  '10': "Isotopes & Radiation",
                  '11': "Materials Science & Technology",
                  '12': "Mathematics & Computation",
                  '13': "Nonproliferation & Nuclear Safeguards",
                  '14': "Nuclear Criticality Safety",
                  '15': "Nuclear Installations Safety",
                  '16': "Operations & Power",
                  '17': "Policy",
                  '18': "Radiation Protection & Shielding",
                  '19': "Robotics & Remote Systems",
                  '20': "Reactor Physics",
                  '21': "Student Sections Activities",
                  '22': "Thermal Hydraulics/Fluids",
                  '23': "Special Session: Radiochemistry"
              }

#old_headers = ['paper id', 'first name', 'last name', 'institution', 'track', 'title']

new_headers = "paper id, First Name, Last Name, Institution, Affiliation, Track, Podium?, title, Follow Up"


title_t = "{1} {2}, {3}. {7}. {9}"

def main():

  papers = []
  posters = []

  reader = csv.reader(open('data_processed_final.csv','r'), delimiter=';')
  for row in reader:
    if not row[0] or row[0] == "paper id": continue

    row.append(tracks[row[5]])
    
    row  = [item.strip() for item in row]
    
    if row[6] == "1":
      papers.append(row+[title_t.format(*row)])
    else:
      posters.append(row+[title_t.format(*row)])


  os.system("rm -rf source/authors source/tracks source/insts")
  os.mkdir('source/authors')
  os.mkdir('source/tracks')
  os.mkdir('source/insts')
  
  make_docs(papers,'podium')
  make_docs(posters,'poster')


################################################################################
################################################################################
################################################################################
################################################################################
def make_docs(papers,prefix):

  titlepre = list(prefix)
  titlepre[0] = 'P'
  titlepre.append('s')
  titlepre = "".join(titlepre)

################################################################################
################################################################################
  # author
  names = []
  docs = []
  title = "{0} - First Author's Name".format(titlepre)
  outstr = """ :ref:`Back to Index <index>`

{0}
{1}

.. toctree::

""".format(title,'-'*len(title))
  papers = sorted(papers, key=lambda x: x[2])
  for paper in papers:
    if not (paper[1],paper[2]) in names:
      names.append((paper[1],paper[2]))
      outstr += "   {2}, {3} <authors/{1}_auth_{0}>\n".format(len(names)-1,prefix,paper[2],paper[1])
      name = "{0}, {1} - {2}".format(paper[2],paper[1],titlepre)
      docs.append(""" :ref:`Back to Index <index>`

{0}
{1}

* `{2} <../_static/docs/{3}.pdf>`_
""".format(name,'-'*len(name),paper[-1],paper[0]))
    else:
      docs[-1] += "* `{0} <../_static/docs/{1}.pdf>`_\n".format(paper[-1],paper[0])
  with open('source/{0}_author.rst'.format(prefix),'w') as fh:
    fh.write(outstr)
  for i,authdoc in enumerate(docs):
    with open('source/authors/{1}_auth_{0}.rst'.format(i,prefix),'w') as fh:
      fh.write(authdoc)
    
################################################################################
################################################################################
  # institution
  insts = []
  docs = []
  title = "{0} - First Author's Institution".format(titlepre)
  outstr = """ :ref:`Back to Index <index>`

{0}
{1}

.. toctree::

""".format(title,'-'*len(title))
  papers = sorted(papers, key=lambda x: x[3])
  for paper in papers:
    if not paper[3] in insts:
      insts.append(paper[3])
      outstr += "   {2} <insts/{1}_inst_{0}>\n".format(len(insts)-1,prefix,paper[3])
      if not paper[3]: paper[3] = 'None'
      docs.append(""" :ref:`Back to Index <index>`

{0}
{1}

* `{2} <../_static/docs/{3}.pdf>`_
""".format(paper[3] + ' - '+titlepre,'-'*len(paper[3] + ' - '+titlepre),paper[-1],paper[0]))
    else:
      docs[-1] += "* `{0} <../_static/docs/{1}.pdf>`_\n".format(paper[-1],paper[0])
  with open('source/{0}_inst.rst'.format(prefix),'w') as fh:
    fh.write(outstr)
  for i,authdoc in enumerate(docs):
    with open('source/insts/{1}_inst_{0}.rst'.format(i,prefix),'w') as fh:
      fh.write(authdoc)

################################################################################
################################################################################
  # All
  title = "{0} - All".format(titlepre)
  outstr = """ :ref:`Back to Index <index>`

{0}
{1}

.. toctree::

""".format(title,'-'*len(title))
  papers = sorted(papers, key=lambda x: x[2])
  for paper in papers:
    outstr += "* `{0} <_static/docs/{1}.pdf>`_\n".format(paper[-1],paper[0])
  with open('source/{0}_title.rst'.format(prefix),'w') as fh:
    fh.write(outstr)

################################################################################
################################################################################
  # track
  papers = sorted(papers, key=lambda x: x[2]) # sort by author
  title = "{0} - Techincal Track".format(titlepre)
  outstr = """ :ref:`Back to Index <index>`

{0}
{1}

.. toctree::

""".format(title,'-'*len(title))
  for i in range(24):
    outstr += "    {2} <tracks/{1}_tr{0}>\n".format(i,prefix,tracks[str(i)])
  with open('source/{0}_track.rst'.format(prefix),'w') as fh:
    fh.write(outstr)
  for i in range(24):
    outstr = """ :ref:`Back to Index <index>`

{0}
{1}

""".format(tracks[str(i)]+' - '+titlepre,'-'*len(tracks[str(i)]+' - '+titlepre))
    for paper in papers:
      if paper[5] == str(i):
        outstr += "* `{0} <../_static/docs/{1}.pdf>`_\n".format(paper[-1],paper[0])
    with open('source/tracks/{1}_tr{0}.rst'.format(i,prefix),'w') as fh:
      fh.write(outstr)
      
if __name__ == "__main__":
  main()
