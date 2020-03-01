#!/bin/bash

TOOLS=${TOOLS:-~/work/odoo-dev/tools}
ds=$(date "+%Y-%m-%d-%H-%M-%S")

for p in rental_* sale_rental*; do
  m=${p}/__manifest__.py
  docdir=${p}/README
  shtmldir=${p}/static/description
  shtmlfn=${shtmldir}/index.html
  descfn=${docdir}/DESCRIPTION.rst
  mkdir -p ${docdir} || {
    echo "error: cannot create ${docdir}, continuing with next package..."
    continue
  }
  mkdir -p ${shtmldir} || {
    echo "error: cannot create ${shtmldir}, continuing with next package..."
    continue
  }
  if grep -q "'name'" ${m}; then
    name=$(${TOOLS}/get_openerp_info.py -f ${m} -a name -p '' | sed -e 's/^\.$//' -e 's/|//g')
  else
    echo "error: module name not found, continuing with next package..."
    continue
  fi
  if grep -q "'summary'" ${m}; then
    summary=$(${TOOLS}/get_openerp_info.py -f ${m} -a summary -p '' | sed -e 's/^\.$//' -e 's/|//g')
  else
    echo "error: module summary not found, continuing with next package..."
    continue
  fi
  if grep -q "'description'" ${m}; then
    description=$(${TOOLS}/get_openerp_info.py -f ${m} -a description -p '' | sed -e 's/^\.$//' -e 's/|//g')
  else
    description='TODO'
  fi
  {
    echo "${name}"
    echo "==========================================="
    echo ""
    echo "*This file has been generated on ${ds}. Changes to it will be overwritten.*"
    echo ""
    echo "Summary"
    echo "-------"
    echo ""
    echo "${summary}"
    echo ""
    echo "Description"
    echo "-----------"
    echo ""
    echo "${description}"
    echo ""
  } > ${descfn}
  rst2html.py ${descfn} ${shtmlfn}
  git add ${docdir}
  git add ${shtmldir}
done
rm -f */*.tmp
