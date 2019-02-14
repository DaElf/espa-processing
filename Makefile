#-----------------------------------------------------------------------------
# Makefile
#
# Project Name: ESPA RPM Building
#-----------------------------------------------------------------------------
.PHONY: check-environment all base schemas science install clean espa-release-info espa-release-aux-info product-formatter product-formatter-schemas l2qa-tools elevation reprojection spectral-indices surface-water-extent surface-water-extent-dswe surface-water-extent-cfbwd surface-reflectance surface-reflectance-ledaps surface-reflectance-ledaps-aux surface-reflectance-lasrc surface-reflectance-lasrc-aux surface-temperature surface-temperature-rit surface-temperature-aux plotting

all:

base: product-formatter

schemas: product-formatter-schemas

science: l2qa-tools elevation reprojection spectral-indices surface-water-extent surface-water-extent-dswe surface-water-extent-cfbwd surface-reflectance surface-reflectance-ledaps surface-reflectance-lasrc surface-temperature surface-temperature-rit plotting

lasrc-aux: surface-reflectance-lasrc-aux
ledaps-aux: surface-reflectance-ledaps-aux
narr-aux: surface-temperature-aux
auxiliary: narr-aux lasrc-aux ledaps-aux

install:

clean:

#-----------------------------------------------------------------------------
espa-release-info: check-environment
	rpmbuild -bb --clean specs/espa-release-info.spec

espa-release-aux-info: check-environment
	rpmbuild -bb --clean specs/espa-release-aux-info.spec

#-----------------------------------------------------------------------------
#-------- BASE LIBRARIES
product-formatter: check-environment
	rpmbuild -bb --clean specs/espa-product-formatter.spec

product-formatter-schemas: check-environment
	rpmbuild -bb --clean specs/espa-product-formatter-schemas.spec

l2qa-tools: check-environment
	rpmbuild -bb --clean specs/espa-l2qa-tools.spec

#-------- ELEVATION
elevation: check-environment
	rpmbuild -bb --clean specs/espa-elevation.spec

#-------- REPROJECTION
reprojection: check-environment
	rpmbuild -bb --clean specs/espa-reprojection.spec

#-------- SPECTAL INDICES
spectral-indices: check-environment
	rpmbuild -bb --clean specs/espa-spectral-indices.spec

#-------- SURFACE WATER EXTENT
surface-water-extent: check-environment
	rpmbuild -bb --clean specs/espa-surface-water-extent.spec

surface-water-extent-dswe: check-environment
	rpmbuild -bb --clean specs/espa-surface-water-extent-dswe.spec

surface-water-extent-cfbwd: check-environment
	rpmbuild -bb --clean specs/espa-surface-water-extent-cfbwd.spec

#-------- SURFACE REFLECTANCE
surface-reflectance: check-environment
	rpmbuild -bb --clean specs/espa-surface-reflectance.spec

surface-reflectance-ledaps: check-environment
	rpmbuild -bb --clean specs/espa-surface-reflectance-ledaps.spec

surface-reflectance-ledaps-aux: check-environment
	rpmbuild -bb --clean specs/espa-surface-reflectance-ledaps-aux.spec

surface-reflectance-lasrc: check-environment
	rpmbuild -bb --clean specs/espa-surface-reflectance-lasrc.spec

surface-reflectance-lasrc-aux: check-environment
	rpmbuild -bb --clean specs/espa-surface-reflectance-lasrc-aux.spec

#-------- SURFACE TEMPERATURE
surface-temperature: check-environment
	rpmbuild -bb --clean specs/espa-surface-temperature.spec

surface-temperature-rit: check-environment
	rpmbuild -bb --clean specs/espa-surface-temperature-rit.spec

surface-temperature-aux: check-environment
	rpmbuild -bb --clean specs/espa-surface-temperature-aux.spec

#-------- STATISTICS AND PLOTTING
plotting: check-environment
	rpmbuild -bb --clean specs/espa-plotting.spec

#-----------------------------------------------------------------------------
check-environment:
ifndef PREFIX
    $(error Environment variable PREFIX is not defined)
endif

