#!/bin/bash -eux

is_python3() {
        python --version |& grep -qF 3.
}

python -m pgtoolkit.hba data/pg_hba.conf
! (python -m pgtoolkit.hba data/pg_hba_bad.conf && exit 1)

python -m pgtoolkit.pgpass data/pgpass
! (python -m pgtoolkit.pgpass data/pgpass_bad && exit 1)

python -m pgtoolkit.service data/pg_service.conf
! (python -m pgtoolkit.service data/pg_service_bad.conf && exit 1)

python -m pgtoolkit.log '%m [%p]: [%l-1] app=%a,db=%d%q,client=%h,user=%u ' data/postgresql.log
if is_python3 ; then
        scripts/profile-log
fi
