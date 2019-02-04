#!/bin/bash/python
__version__ = 0.321
__author__ = 'alastair.maxwell@glasgow.ac.uk'

## imports
import os
import pkg_resources
from shutil import move
from fadapa import Fadapa
from shutil import copyfile
from tempfile import mkstemp
from os import fdopen, remove
from ..__backend import mkdir_p

class genHTML:
    def __init__(self, scalehdResults=None, shdVersion=None, jobLabel=None, outputPath=None):

        """
        docstring todo
        """

        ## class attributes
        self.instance_objects = scalehdResults
        self.WEB_BASE = os.path.dirname(os.path.abspath(__file__))
        self.TEMPLATES_BASE = os.path.join(self.WEB_BASE, 'templates')
        self.OUTPUT_ROOT = outputPath
        self.HTML_FILE = os.path.join(outputPath,'{}{}'.format(jobLabel, 'WebResults.html')) ## actual HTML page
        self.HTML_MEDIA_ROOT = os.path.join(outputPath, jobLabel+'Resources') ## for sample based graphs.. etc

        ## make directories cos they won't exist fam
        for dir in [self.OUTPUT_ROOT, self.HTML_MEDIA_ROOT]:
            if not os.path.exists(dir):
                mkdir_p(dir)

        ## Collate ScaleHD results in meaningful way for HTML
        self.SAMPLES = []; self.get_processed_samples()

        ## Base HTML template for SHD output
        ## items to be filled with generated HTML strings from templates
        ## before being placed into their respective HTML locations
        base_template = os.path.join(self.TEMPLATES_BASE, 'base.html')
        cag_summary = self.get_summary('CAG'); ccg_summary = self.get_summary('CCG')
        allelesummary_javascript = self.implement_summaries(jobLabel, cag_summary, ccg_summary) #send summary data to scalehd.JS file
        styling_str = self.get_styling() #CSS
        script_str = self.get_javascript() #Javascript
        version_str = shdVersion # Get ScaleHD versionx
        instancelabel_str = jobLabel # Get ScaleHD jobLabel
        lists_str = self.get_lists_html() # Get sample list of which SHD processed
        analysis_str = self.get_seqdata() # Get SubStage information for each sample
        ##copy footer to results web dir
        footer_img = pkg_resources.resource_filename(__name__, 'img/footer.png')
        target_img = os.path.join(self.HTML_MEDIA_ROOT, 'footer.png'); copyfile(footer_img, target_img)
        footer_str = '<img src=\"{}" alt=\"UoG + CHDI\"><br/>'.format(target_img)

        ## WRITE EVERYTHING COLLECTED TO BASE HTML TEMPLATE
        ## THIS IS THE FINAL OUTPUT CURATION STAGE
        base_template = os.path.join(self.TEMPLATES_BASE, 'base.html')
        f = open(base_template, 'r')
        output = ''

        for line in f:
            line = line.format(CSS=styling_str,
                               SAMPLE_LIST=lists_str, shd_version=version_str,
                               instance_label=instancelabel_str, FOOTERIMG = footer_str,
                               SEQDATA=analysis_str, JAVASCRIPT=script_str)
            output = '{0}{1}'.format(output, line)
        f.close()

        ## Write to final output HMTL
        with open(self.HTML_FILE,'w') as outfi:
            outfi.write(output)

    def get_processed_samples(self):
        for individual in self.instance_objects:
            self.SAMPLES.append(individual.get_label())

    def get_summary(self, triplet):

        ## CAG
        cag_blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if triplet == 'CAG':
            for individual in self.instance_objects:
                try:
                    primary_cag = individual.get_primaryallele().get_cag()
                    secondary_cag = individual.get_secondaryallele().get_cag()
                    for allele in [primary_cag, secondary_cag]:
                        index = 0
                        while index < len(cag_blank):
                            if index == allele:
                                cag_blank[index] += 1
                            index += 1
                except AttributeError: ##skip over samples that have no genotype (i.e. failed)
                    pass

            return cag_blank

        ## CCG
        ccg_blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if triplet == 'CCG':
            for individual in self.instance_objects:
                try:
                    primary_ccg = individual.get_primaryallele().get_ccg()
                    secondary_ccg = individual.get_secondaryallele().get_ccg()
                    for allele in [primary_ccg, secondary_ccg]:
                        index = 0
                        while index < len(ccg_blank):
                            if index == allele:
                                ccg_blank[index] += 1
                            index += 1
                except AttributeError:
                    pass

            return ccg_blank

    def implement_summaries(self, jobLabel, cag_summary, ccg_summary):

        ## Target/Templates
        scalehdbase_path = os.path.join(self.TEMPLATES_BASE, 'scalehd_base.js')
        scalehd_out_path = os.path.join(self.WEB_BASE, 'scalehd.js')
        template_path = os.path.join(self.TEMPLATES_BASE, 'alleleSummary.js')

        ## CAG Summary
        f = open(template_path, 'r')
        cag_output = f.read()
        cag_output = cag_output.replace('{TRIPLET_TYPE}','CAGSummaryChart')
        cag_output = cag_output.replace('{LABELS}',"['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200']")
        cag_output = cag_output.replace('{TRIPLET_DISTRIBUTION}', str(cag_summary))
        cag_output = cag_output.replace('{BACKGROUND_COLOUR}', '\"#006110\"')
        cag_output = cag_output.replace('{BORDER_COLOUR}', '\"#009419\"')
        cag_output = cag_output.replace('{CHART_TITLE}', '\"CAG allele distribution for {}\"'.format(jobLabel))
        f.close()

        ## CCG Summary
        f = open(template_path, 'r')
        ccg_output = f.read()
        ccg_output = ccg_output.replace('{TRIPLET_TYPE}','CCGSummaryChart')
        ccg_output = ccg_output.replace('{LABELS}', "['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']")
        ccg_output = ccg_output.replace('{TRIPLET_DISTRIBUTION}', str(ccg_summary))
        ccg_output = ccg_output.replace('{BACKGROUND_COLOUR}', '\"#e100bb\"')
        ccg_output = ccg_output.replace('{BORDER_COLOUR}', '\"#94007b\"')
        ccg_output = ccg_output.replace('{CHART_TITLE}', '\"CCG allele distribution for {}\"'.format(jobLabel))
        f.close()

        ## write to scalehd.js
        f = open(scalehdbase_path, 'r')
        all_output = f.read()
        all_output = all_output.replace('{CAG_FUNCTION}', cag_output)
        all_output = all_output.replace('{CCG_FUNCTION}', ccg_output)
        f.close()
        with open(scalehd_out_path, 'w') as outfi:
            outfi.write(all_output)

    def get_styling(self):
        gridism_path = os.path.join(self.WEB_BASE, 'gridism.css')
        scalehd_path = os.path.join(self.WEB_BASE, 'scalehd.css')
        css_string = ''

        ## gridism styling
        f = open(gridism_path, 'r')
        for line in f:
            css_string += line
        f.close()
        ## scalehd styling
        f = open(scalehd_path, 'r')
        for line in f:
            css_string += line
        f.close()

        css_string = '<style type=\"text/css\">' + css_string + '</style>'
        return css_string

    def get_javascript(self):
        jquery_path = os.path.join(self.WEB_BASE, 'jquery.js')
        scalehd_path = os.path.join(self.WEB_BASE, 'scalehd.js')
        chart_path = os.path.join(self.WEB_BASE, 'chart.js')
        js_string = ''

        ## jquery scripts
        f = open(jquery_path, 'r')
        for line in f:
            js_string += line
        f.close()
        ## scalehd scripts
        f = open(scalehd_path, 'r')
        for line in f:
            js_string += line
        f.close()
        ## chart.js scripts
        f = open(chart_path, 'r')
        for line in f:
            js_string += line
        f.close()

        js_string = '<script type=\"text/javascript\">' + js_string + '</script>'
        return js_string

    def get_lists_html(self):

        """
        docstring todo
        """

        list_template = os.path.join(self.TEMPLATES_BASE, 'list.html')
        return_str = ''

        f = open(list_template, 'r')

        for sequence in self.SAMPLES:
            for line in f:
                line = line.format(ID=sequence)
                return_str = '{0}{1}'.format(return_str, line)

            f.seek(0)

        f.close()
        return return_str

    def get_seqdata(self):

        """
        docstring todo
        """

        seqdata_template = os.path.join(self.TEMPLATES_BASE, 'sequencedata.html')
        return_str = ''

        f = open(seqdata_template, 'r')
        for sequence in self.SAMPLES:

            targetObject = None
            ## Select object from instance results
            for x in self.instance_objects:
                if x.get_label() == sequence:
                    targetObject = x

            ## HEADLINE INFORMATION
            primary_cag = ''; primary_ccg = ''; primary_structurelabel = ''; primary_structure = ''; primary_confidence = ''
            secondary_cag = ''; secondary_ccg = ''; secondary_structurelabel = ''; secondary_structure = ''; secondary_confidence = ''

            try:
                primary_allele = targetObject.get_primaryallele()
                primary_cag = primary_allele.get_cag(); primary_ccg = primary_allele.get_ccg()
                primary_structurelabel = primary_allele.get_allelestatus(); primary_structure = primary_allele.get_allelegenotype()
                primary_confidence = primary_allele.get_alleleconfidence()

                secondary_allele = targetObject.get_secondaryallele()
                secondary_cag = secondary_allele.get_cag(); secondary_ccg = secondary_allele.get_ccg()
                secondary_structurelabel = secondary_allele.get_allelestatus(); secondary_structure = secondary_allele.get_allelegenotype()
                secondary_confidence = secondary_allele.get_alleleconfidence()
            except AttributeError:
                pass ## skip over samples that failed genotyping

            ## replace with results from ScaleHD for the current sample
            test_seqqc = self.get_sampleQC(sequence)
            test_seqaln = self.get_sampleALN(sequence)
            test_gtype = self.get_sampleGTYPE(sequence)

            for line in f:
                line = line.format(
                ID=sequence,
                A1_CAG=primary_cag, A1_CCG=primary_ccg, A1_STRUCTURELABEL=primary_structurelabel, A1_STRUCTURE=primary_structure, A1_CONFIDENCE=primary_confidence,
                A2_CAG=secondary_cag, A2_CCG=secondary_ccg, A2_STRUCTURELABEL=secondary_structurelabel, A2_STRUCTURE=secondary_structure, A2_CONFIDENCE=secondary_confidence,
                SEQ_QC=test_seqqc, SEQ_ALN=test_seqaln, GTYPE=test_gtype)
                return_str = '{0}{1}'.format(return_str, line)
            f.seek(0)
        f.close()

        return return_str

    def get_sampleQC(self, currSample):

        targetObject = None
        ## Select object from instance results
        for x in self.instance_objects:
            if x.get_label() == currSample:
                targetObject = x

        ##################################################################
        ## Check for Trimming report! scrape data and format if present ##
        ##################################################################
        forwardTrimReport = targetObject.get_trimreport()[0]; forwardTrimString = ''
        reverseTrimReport = targetObject.get_trimreport()[1]; reverseTrimString = ''
        try:
            with open(forwardTrimReport, 'r') as infi:
                forwardTrimString=infi.read()
            forwardTrimString = self.format_trimming(forwardTrimString)
        except Exception, e:
            forwardTrimString = 'We could not find/process a forward trimming report! Exception raised: {}'.format(e)
        try:
            with open(reverseTrimReport, 'r') as infi:
                reverseTrimString=infi.read()
            reverseTrimString = self.format_trimming(reverseTrimString)
        except Exception, e:
            reverseTrimString = 'We could not find/process a reverse trimming report! Exception raised: {}'.format(e)

        ################################################################
        ## Check for FastQC report! scrape data and format if present ##
        ################################################################
        forwardFQCReport = targetObject.get_fqcreport()[0]; forwardFQCString = ''
        try:
            forwardFQCString = self.format_fastqc(forwardFQCReport, currSample)
        except Exception, e:
            forwardFQCString = 'We could not find/process a FastQC report! Exception raised: {}'.format(e)

        ###################################################################
        ## Apply scraped and formatted data into HTML template for SeqQC ##
        ###################################################################
        qc_template = os.path.join(self.TEMPLATES_BASE, 'seqqc.html')
        f = open(qc_template, 'r')
        qc_return = ''
        for line in f:
            line = line.format(ID=currSample, FORWARD_TRIM=forwardTrimString, REVERSE_TRIM=reverseTrimString, FASTQC=forwardFQCString)
            qc_return = '{0}{1}'.format(qc_return, line)
        f.close()

        return qc_return

    def format_trimming(self, rawData):

        ## Trimming template
        trim_template = os.path.join(self.TEMPLATES_BASE, 'trim.html')

        ## First get technical summary; replace python newline with HTML break, remove start/end breaks
        techSummary = rawData.split('=== Summary ===')[0]
        techSummary = techSummary.replace('\n', '<br />').lstrip('<br />').rstrip('<br />')

        ## Trimming Summary; replace python newline with HTML break, remove start/end breaks
        trimSummary = rawData.split('=== Summary ===')[1].split('=== Adapter 1 ===')[0]
        trimSummary = trimSummary.replace('\n', '<br />').lstrip('<br />').rstrip('<br />')
        trimSummary = trimSummary.replace('<br /><br />', '<br />')

        ## Adapter summary; replace python newline with HTML break, remove start/end breaks
        adapterSummary = rawData.split('=== Adapter 1 ===')[1].split('Overview of removed sequences')[0]
        adapterSummary = adapterSummary.replace('\n', '<br />').lstrip('<br />').rstrip('<br />')
        adapterSummary = adapterSummary.replace(';', '<br />')

        trim_return = ''
        f = open(trim_template, 'r')
        for line in f:
            line = line.format(TECHNICAL=techSummary, SUMMARY=trimSummary, ADAPTER=adapterSummary)
            trim_return = '{0}{1}'.format(trim_return, line)
        f.close()

        ## Return formatted trimming report
        return trim_return

    def format_fastqc(self, rawDataPath, currSample):

        ## FastQC templates
        fastqc_template = os.path.join(self.TEMPLATES_BASE, 'fastqc.html')

        ## just fuckin lump it all in there for now and figure out what you want to format next
        fqc_object = Fadapa(rawDataPath)
        print '\n hello we are attempting to format FastQC data'

        ## Module status data
        module_summary = fqc_object.summary()
        module_stats = module_summary[1][0]; module_pbsq = module_summary[2][0]; module_ptsq = module_summary[3][0];
        module_psqs = module_summary[4][0]; module_pbsc = module_summary[5][0]; module_psgcc = module_summary[6][0];
        module_pbnc = module_summary[7][0]; module_seqlendist = module_summary[8][0]; module_seqdup = module_summary[9][0];
        module_overrep = module_summary[10][0]; module_adapter = module_summary[11][0]

        ## Basic statistics data
        basic_stats = fqc_object.clean_data('Basic Statistics')
        file_name = basic_stats[1][1]; file_type = basic_stats[2][1]; encoding = basic_stats[3][1]
        total_sequences = basic_stats[4][1]; poor_quality = basic_stats[5][1]; seq_len = basic_stats[6][1]
        gc_pcnt = basic_stats[7][1]

        ## Per Base Pair Sequence Quality
        ## blue line - mean quality
        ## yellow box (lower quart to upper quart)
        ## error bars (10th pcnt to 90th pcnt)
        ## red line - median value
        ##print fqc_object.clean_data('Per base sequence quality')

        ## Per Base Pair N Content

        ## Sequence Length Distribution


        print 'sending >>> ', currSample

        fqc_return = ''
        f = open(fastqc_template, 'r')
        for line in f:
            line = line.format(
            MODULE_STATS = module_stats, MODULE_PBSQ = module_pbsq, MODULE_PTSQ = module_ptsq,
            MODULE_PSQS = module_psqs, MODULE_PBSC = module_pbsc, MODULE_PSGCC = module_psgcc,
            MODULE_PBNC = module_pbnc, MODULE_SEQLENDIST = module_seqlendist, MODULE_SEQDUP = module_seqdup,
            MODULE_OVERREP = module_overrep, MODULE_ADAPTER = module_adapter,
            FQC_FILENAME = file_name, FQC_FILETYPE = file_type, FQC_ENCODING = encoding,
            FQC_TOTALSEQ = total_sequences, FQC_POORQUAL = poor_quality, FQC_SEQLEN = seq_len,
            FQC_GCPCNT = gc_pcnt,
            FASTQCREPORT = 'hello working on it'
            )
            fqc_return = '{0}{1}'.format(fqc_return, line)
        f.close()

        ## return formatted FastQC report
        return fqc_return

    def get_sampleALN(self, currSample):
        return "testALN"

    def get_sampleGTYPE(self, currSample):
        return "testGTYPE"
