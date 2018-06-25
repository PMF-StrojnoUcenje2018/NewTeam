import os
import json
import pandas as pd
import numpy as np
import re

def get_dataframe (file_list):


    #---------------------------------------------#
    # Stvaranje NumPy arraya                      #
    #---------------------------------------------#
    
    N = len(file_list)

    # entries
    log_entries_num = np.empty(N, dtype = np.float32)
    log_entries_num.fill(-1)

    #   info
    #    file
    log_max_entry_size = np.empty(N, dtype = np.float32)
    log_max_entry_size.fill(-1)

    log_average_entry_size = np.empty(N, dtype = np.float32)
    log_average_entry_size.fill(-1)

    log_sum_entry_size = np.empty(N, dtype = np.float32)
    log_sum_entry_size.fill(-1)

    log_repeated_entry_sizes = np.empty(N, dtype = np.float32)
    log_repeated_entry_sizes.fill(-1)

    max_entry_entropy = np.empty(N, dtype = np.float32)
    max_entry_entropy.fill(-1)

    average_entry_entropy = np.empty(N, dtype = np.float32)
    average_entry_entropy.fill(-1)

    average2_entry_entropy = np.empty(N, dtype = np.float32)
    average2_entry_entropy.fill(-1)

    #    validation
    warnings_num = np.empty(N, dtype = np.int16)
    warnings_num.fill(-1)

    #   metadata
    non_empty_metadatas = np.empty(N, dtype = np.int16)
    non_empty_metadatas.fill(-1)

    #    application
    #      dosHeader
    max_elfa_new = np.empty(N, dtype = np.int32)
    max_elfa_new.fill(-1)

    #      fileHeader
    time_date_stamp_min_year = np.empty(N, dtype = np.int16)
    time_date_stamp_min_year.fill(-1)

    time_date_stamp_max_year = np.empty(N, dtype = np.int16)
    time_date_stamp_max_year.fill(-1)

    max_opt_header_size = np.empty(N, dtype = np.int16)
    max_opt_header_size.fill(-1)

    characteristics_num = np.empty(N, dtype = np.int16)
    characteristics_num.fill(-1)

    #      optionalHeader
    is_checksum_valid = np.zeros(N, dtype = np.bool)

    log_max_size_of_initialized_data = np.empty(N, dtype = np.float32)
    log_max_size_of_initialized_data.fill(-1)

    log_max_size_of_uninitialized_data = np.empty(N, dtype = np.float32)
    log_max_size_of_uninitialized_data.fill(-1)

    log_max_stack_reserve = np.empty(N, dtype = np.float32)
    log_max_stack_reserve.fill(-1)

    log_max_heap_reserve = np.empty(N, dtype = np.float32)
    log_max_heap_reserve.fill(-1)

    data_notnull_directories_num = np.empty(N, dtype = np.int16)
    data_notnull_directories_num.fill(-1)

    #      sections
    first_section_name = np.empty(N, dtype = np.int8)
    first_section_name.fill(-1)

    first_section_wec_code = np.empty(N, dtype = np.int8)
    first_section_wec_code.fill(-1)

    log_sections_num = np.empty(N, dtype = np.float32)
    log_sections_num.fill(-1)

    log_nonstandard_section_names_num = np.empty(N, dtype = np.float32)
    log_nonstandard_section_names_num.fill(-1)

    log_sections_rwe_num = np.empty(N, dtype = np.float32)
    log_sections_rwe_num.fill(-1)

    log_sections_rwec_num = np.empty(N, dtype = np.float32)
    log_sections_rwec_num.fill(-1)

    last_section_discardable = np.zeros(N, dtype = np.bool)

    last_section_suspicious_name = np.empty(N, dtype = np.int8)
    last_section_suspicious_name.fill(-1)

    log_max_section_size = np.empty(N, dtype = np.float32)
    log_max_section_size.fill(-1)

    log_average_section_size = np.empty(N, dtype = np.float32)
    log_average_section_size.fill(-1)

    log_zero_size_sections_num = np.empty(N, dtype = np.float32)
    log_zero_size_sections_num.fill(-1)

    first_section_entropy = np.empty(N, dtype = np.float32)
    first_section_entropy.fill(-1)

    max_section_entropy = np.empty(N, dtype = np.float32)
    max_section_entropy.fill(-1)

    average2_section_entropy = np.empty(N, dtype = np.float32)
    average2_section_entropy.fill(-1)

    log_max_section_suspiciousness = np.empty(N, dtype = np.float32)
    log_max_section_suspiciousness.fill(-1)

    #      imports
    log_imports_num = np.empty(N, dtype = np.float32)
    log_imports_num.fill(-1)

    log_max_api_list_size = np.empty(N, dtype = np.float32)
    log_max_api_list_size.fill(-1)

    log_average_api_list_size = np.empty(N, dtype = np.float32)
    log_average_api_list_size.fill(-1)

    log_sum_api_list_size = np.empty(N, dtype = np.float32)
    log_sum_api_list_size.fill(-1)

    #      codeViews
    contains_codeviews = np.zeros(N, dtype = np.bool)

    #      overlay
    log_overlay_size = np.empty(N, dtype = np.float32)
    log_overlay_size.fill(-1)

    entry_minus_sections_minus_overlay = np.empty(N, dtype = np.float32)
    entry_minus_sections_minus_overlay.fill(-1)

    #      richHeader
    rich_header_valid = np.empty(N, dtype = np.int8)
    rich_header_valid.fill(-1)

    log_sum_rich_header_size = np.empty(N, dtype = np.float32)
    log_sum_rich_header_size.fill(-1)

    log_rich_header_entries_num = np.empty(N, dtype = np.float32)
    log_rich_header_entries_num.fill(-1)

    log_rich_header_count_max = np.empty(N, dtype = np.float32)
    log_rich_header_count_max.fill(-1)

    log_rich_header_count_avg = np.empty(N, dtype = np.float32)
    log_rich_header_count_avg.fill(-1)

    log_rich_header_count_sum = np.empty(N, dtype = np.float32)
    log_rich_header_count_sum.fill(-1)

    #    protection
    protection = np.zeros(N, dtype = np.bool)

    #    certificate
    certificate = np.zeros(N, dtype = np.bool)

    #   classification
    classification = np.empty(N, dtype = np.int8)
    classification.fill(-1)

    #   tags
    log_num_tags_graylisting = np.empty(N, dtype = np.float32)
    log_num_tags_graylisting.fill(-1)

    log_num_tags_entropy = np.empty(N, dtype = np.float32)
    log_num_tags_entropy.fill(-1)
    
    log_sum_tag_entropy_entry_sizes = np.empty(N, dtype = np.float32)
    log_sum_tag_entropy_entry_sizes.fill(-1)

    cert_malformed = np.zeros(N, dtype = np.bool)

    # relationships
    log_relationships_num = np.empty(N, dtype = np.float32)
    log_relationships_num.fill(-1)


    #---------------------------------------------#
    # Čitanje JSON datoteka i izvlačenje atributa #
    #---------------------------------------------#
    
    DEBUG = False

    standard_section_names = {".text", ".data", ".rdata", ".idata", ".edata", ".rsrc", ".bss", ".crt", ".tls",
                              ".reloc", ".sdata", ".srdata", ".pdata", ".debug$S", ".debug$T", ".debug$P",
                              ".drectve", ".didat", ".imports"}
    
    for i, filename in enumerate(file_list):
        json_data = open(filename, encoding='utf-8').read()
        exe_data = json.loads(json_data)


        try:
            x = np.log(1 + len(exe_data["coreReport"]["entries"]["entry_list"]))
            log_entries_num[i] = x
        except:
            if DEBUG:
                print('Aerr' + str(i), end=' ', flush=True)
        
        
        # entry sizes
        try:
            entry_sizes = [int(li["info"]["file"]["size"], 0) for li in
                           exe_data["coreReport"]["entries"]["entry_list"]]
        except:
            if DEBUG:
                print('Derr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + max(entry_sizes))
            log_max_entry_size[i] = x
        except:
            if DEBUG:
                print('Eerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + np.mean(entry_sizes))
            log_average_entry_size[i] = x
        except:
            if DEBUG:
                print('Ferr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(entry_sizes))
            log_sum_entry_size[i] = x
        except:
            if DEBUG:
                print('Gerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + len(entry_sizes) - len(set(entry_sizes)))
            log_repeated_entry_sizes[i] = x
        except:
            if DEBUG:
                print('Herr' + str(i), end=' ', flush=True)
        
        
        # entry entropies
        try:
            entry_entropies = [float(li["info"]["file"]["entropy"]) for li in
                               exe_data["coreReport"]["entries"]["entry_list"]]
        except:
            if DEBUG:
                print('Ierr' + str(i), end=' ', flush=True)
        
        try:
            x = max(entry_entropies)
            max_entry_entropy[i] = x
        except:
            if DEBUG:
                print('Jerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.mean(entry_entropies)
            average_entry_entropy[i] = x
        except:
            if DEBUG:
                print('Kerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.sqrt(np.average(np.array(entry_entropies) ** 2,
                                            weights = entry_sizes))
            average2_entry_entropy[i] = x
        except:
            if DEBUG:
                print('Lerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = 0
            for li in exe_data["coreReport"]["entries"]["entry_list"]:
                if "warnings" in li["info"]:
                    x += len(li["info"]["warnings"]["warning_list"])
                if "validation" in li["info"] and "warnings" in li["info"]["validation"]:
                    x += len(li["info"]["validation"]["warnings"]["warning_list"])
            warnings_num[i] = x
        except:
            if DEBUG:
                print('Merr' + str(i), end=' ', flush=True)
        
        
        try:
            metadatas = ([li["metadata"] for li in
                          exe_data["coreReport"]["entries"]["entry_list"]
                          if li["metadata"]])
        except:
            if DEBUG:
                print('Nerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = len(metadatas)
            non_empty_metadatas[i] = x
        except:
            if DEBUG:
                print('Oerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = (max(int(li["application"]["pe"]["dosHeader"]["eLFANew"],0)
                     for li in metadatas))
            max_elfa_new[i] = x
        except:
            if DEBUG:
                print('Perr' + str(i), end=' ', flush=True)
        
        
        try:
            x = (min(int(li["application"]["pe"]["fileHeader"]["timeDateStamp"].split()[-1])
                     for li in metadatas))
            time_date_stamp_min_year[i] = x
        except:
            if DEBUG:
                print('Qerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = (max(int(li["application"]["pe"]["fileHeader"]["timeDateStamp"].split()[-1])
                     for li in metadatas))
            time_date_stamp_max_year[i] = x
        except:
            if DEBUG:
                print('Rerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = (max(int(li["application"]["pe"]["fileHeader"]["sizeOfOptionalHeaders"],0)
                     for li in metadatas))
            max_opt_header_size[i] = x
        except:
            if DEBUG:
                print('Serr' + str(i), end=' ', flush=True)
        
        
        try:
            x = len(set.union(*[set(li["application"]["pe"]["fileHeader"]["characteristics"]
                                 ["characteristic_list"]) for li in metadatas]))
            characteristics_num[i] = x
        except:
            if DEBUG:
                print('Terr' + str(i), end=' ', flush=True)
        
        
        try:
            x = (all(li["application"]["pe"]["optionalHeader"]["isChecksumValid"] == "true"
                     for li in metadatas))
            is_checksum_valid[i] = x
        except:
            if DEBUG:
                print('Uerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + max(int(li["application"]["pe"]["optionalHeader"]
                                   ["sizeOfInitializedData"],0)
                               for li in metadatas))
            log_max_size_of_initialized_data[i] = x
        except:
            if DEBUG:
                print('Verr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + max(int(li["application"]["pe"]["optionalHeader"]
                                   ["sizeOfUninitializedData"],0)
                               for li in metadatas))
            log_max_size_of_uninitialized_data[i] = x
        except:
            if DEBUG:
                print('Werr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + max(int(li["application"]["pe"]["optionalHeader"]
                                   ["sizeOfStackReserve"],0)
                               for li in metadatas))
            log_max_stack_reserve[i] = x
        except:
            if DEBUG:
                print('Xerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + max(int(li["application"]["pe"]["optionalHeader"]
                                   ["sizeOfHeapReserve"],0)
                               for li in metadatas))
            log_max_heap_reserve[i] = x
        except:
            if DEBUG:
                print('Yerr' + str(i), end=' ', flush=True)
        
        
        try:
            x = (sum(sum(1 for lii in li["application"]["pe"]["optionalHeader"]
                         ["dataDirectories"]["dataDirectory_list"]
                         if int(lii["size"],0)!=0)
                     for li in metadatas
                     if "dataDirectories" in li["application"]["pe"]["optionalHeader"]))
            data_notnull_directories_num[i] = x
        except:
            if DEBUG:
                print('Zerr' + str(i), end=' ', flush=True)
                
        
        # sections
        try:
            sections = []
            for li in metadatas:
                sections += li["application"]["pe"]["sections"]["section_list"]
        except:
            if DEBUG:
                print('A1err' + str(i), end=' ', flush=True)
        
        
        try:
            if "name" in sections[0]:
                if sections[0]["name"] == ".text":
                    x = 1
                else:
                    x = 0
            else:
                x = -1
            first_section_name[i] = x
        except:
            if DEBUG:
                print('B1err' + str(i), end=' ', flush=True)
        
        
        try:
            if "flags" in sections[0]:
                x = 0
                if "IMAGE_SCN_MEM_WRITE" in sections[0]["flags"]["flag_list"]:
                    x += 4
                if "IMAGE_SCN_MEM_EXECUTE" in sections[0]["flags"]["flag_list"]:
                    x += 2
                if not "IMAGE_SCN_CNT_CODE" in sections[0]["flags"]["flag_list"]:
                    x += 1
            else:
                x = 1
            first_section_wec_code[i] = x
        except:
            if DEBUG:
                print('BB1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + len(sections))
            log_sections_num[i] = x
        except:
            if DEBUG:
                print('C1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(1 for li in sections if not ("name" in li and
                                                            li["name"] in standard_section_names)))
            log_nonstandard_section_names_num[i] = x
        except:
            if DEBUG:
                print('D1err' + str(i), end=' ', flush=True)
                
        
        try:
            x = np.log(1 + sum(1 for li in sections if
                               "flags" in li and
                               "IMAGE_SCN_MEM_READ" in li["flags"]["flag_list"] and
                               "IMAGE_SCN_MEM_WRITE" in li["flags"]["flag_list"] and
                               "IMAGE_SCN_MEM_EXECUTE" in li["flags"]["flag_list"]))
            log_sections_rwe_num[i] = x
        except:
            if DEBUG:
                print('E1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(1 for li in sections if
                               "flags" in li and
                               "IMAGE_SCN_MEM_READ" in li["flags"]["flag_list"] and
                               "IMAGE_SCN_MEM_WRITE" in li["flags"]["flag_list"] and
                               "IMAGE_SCN_MEM_EXECUTE" in li["flags"]["flag_list"] and
                               "IMAGE_SCN_CNT_CODE" in li["flags"]["flag_list"]))
            log_sections_rwec_num[i] = x
        except:
            if DEBUG:
                print('F1err' + str(i), end=' ', flush=True)
        
        
        try:
            if "flags" in sections[-1]:
                x = "IMAGE_SCN_MEM_DISCARDABLE" in sections[-1]["flags"]["flag_list"]
            else:
                x = False
            last_section_discardable[i] = x
        except:
            if DEBUG:
                print('G1err' + str(i), end=' ', flush=True)
        
        
        try:
            if "name" in sections[-1]:
                if sections[-1]["name"] in standard_section_names:
                    x = 1
                else:
                    x = -1
            else:
                x = 0
            last_section_suspicious_name[i] = x
        except:
            if DEBUG:
                print('GG1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + max(int(li["size"], 0) for li in sections))
            log_max_section_size[i] = x
        except:
            if DEBUG:
                print('H1err' + str(i), end=' ', flush=True)
        
        
        try:
            if sections:
                x = np.log(1 + np.mean([int(li["size"], 0) for li in sections]))
                log_average_section_size[i] = x
        except:
            if DEBUG:
                print('I1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(1 for li in sections if int(li["size"],0) == 0))
            log_zero_size_sections_num[i] = x
        except:
            if DEBUG:
                print('J1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = float(sections[0]["entropy"])
            first_section_entropy[i] = x
        except:
            if DEBUG:
                print('K1err' + str(i), end=' ', flush=True)
        first_section_entropy
        
        
        try:
            x = max(float(li["entropy"]) for li in sections)
            max_section_entropy[i] = x
        except:
            if DEBUG:
                print('L1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.average([float(li["entropy"])**2 for li in sections],
                            weights = [int(li["size"],0) for li in sections])
            average2_section_entropy[i] = x
        except:
            if DEBUG:
                print('M1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + max(int(li["size"],0)/(float(li["entropy"])**2)
                               if float(li["entropy"])>0 else 0 for li in sections))
            log_max_section_suspiciousness[i] = x
        except:
            if DEBUG:
                print('MM1err' + str(i), end=' ', flush=True)


        #imports
        #  keys: names
        #  values: set of APIs
        try:
            imports = {}
            for li in metadatas:
                if "imports" in li["application"]["pe"]:
                    for lii in li["application"]["pe"]["imports"]["import_list"]:
                        if not lii["name"] in imports:
                            imports[lii["name"]] = set()
                        if "api_list" in lii:
                            imports[lii["name"]].update(lii["api_list"])
        except:
            if DEBUG:
                print('N1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + len(imports))
            log_imports_num[i] = x
        except:
            if DEBUG:
                print('O1err' + str(i), end=' ', flush=True)
        
        
        try:
            if imports:
                x = np.log(1 + max(len(val) for val in imports.values()))
            else:
                x = 0
            log_max_api_list_size[i] = x
        except:
            if DEBUG:
                print('P1err' + str(i), end=' ', flush=True)
        
        
        try:
            if imports:
                x = np.log(1 + np.mean([len(val) for val in imports.values()]))
            else:
                x = 0
            log_average_api_list_size[i] = x
        except:
            if DEBUG:
                print('Q1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(len(val) for val in imports.values()))
            log_sum_api_list_size[i] = x
        except:
            if DEBUG:
                print('R1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = any("codeViews" in li["application"]["pe"] for li in metadatas)
            contains_codeviews[i] = x
        except:
            if DEBUG:
                print('S1err' + str(i), end=' ', flush=True)


        try:
            s = 0
            for li in metadatas:
                if "overlay" in li["application"]["pe"]:
                    s += int(li["application"]["pe"]["overlay"]["size"],0)
            x = np.log(1 + s)
            log_overlay_size[i] = x
        except:
            if DEBUG:
                print('T1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = 0
            for li in exe_data["coreReport"]["entries"]["entry_list"]:
                if li["metadata"]:
                    x += int(li["info"]["file"]["size"],0)
                    x -= sum(int(lii["size"],0) for lii in
                             li["metadata"]["application"]["pe"]["sections"]["section_list"])
                    if "overlay" in li["metadata"]["application"]["pe"]:
                        x -= int(li["metadata"]["application"]["pe"]["overlay"]["size"],0)
            entry_minus_sections_minus_overlay[i] = x
        except:
            if DEBUG:
                print('U1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = 1
            for li in metadatas:
                if "richHeader" not in li["application"]["pe"]:
                    x = 0
                elif li["application"]["pe"]["richHeader"]["valid"] == "false":
                    x = -1
                    break
            rich_header_valid[i] = x
        except:
            if DEBUG:
                print('V1err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(int(li["application"]["pe"]["richHeader"]["size"],0)
                               for li in metadatas
                               if "richHeader" in li["application"]["pe"]))
            log_sum_rich_header_size[i] = x
        except:
            if DEBUG:
                print('W1err' + str(i), end=' ', flush=True)


        # richHeader_entries
        try:
            richHeader_entries = []
            for li in metadatas:
                if "richHeader" in li["application"]["pe"]:
                    richHeader_entries += (li["application"]["pe"]["richHeader"]
                                           ["entries"]["entry_list"])
        except:
            if DEBUG:
                print('X1err' + str(i), end=' ', flush=True)
        
        
        try:
            if richHeader_entries:
                x = np.log(1 + len(richHeader_entries))
            else:
                x = 0
            log_rich_header_entries_num[i] = x
        except:
            if DEBUG:
                print('Y1err' + str(i), end=' ', flush=True)
        
        
        try:
            if richHeader_entries:
                x = np.log(1 + max(int(li["count"]) for li in richHeader_entries))
            else:
                x = 0
            log_rich_header_count_max[i] = x
        except:
            if DEBUG:
                print('Z1err' + str(i), end=' ', flush=True)
        
        
        try:
            if richHeader_entries:
                x = np.log(1 + np.mean([int(li["count"])
                                        for li in richHeader_entries]))
            else:
                x = 0
            log_rich_header_count_avg[i] = x
        except:
            if DEBUG:
                print('A2err' + str(i), end=' ', flush=True)
        
        
        try:
            if richHeader_entries:
                x = np.log(1 + sum(int(li["count"]) for li in richHeader_entries))
            else:
                x = 0
            log_rich_header_count_sum[i] = x
        except:
            if DEBUG:
                print('B2err' + str(i), end=' ', flush=True)
        
        
        try:
            x = all("protection" in li for li in metadatas)
            protection[i] = x
        except:
            if DEBUG:
                print('C2err' + str(i), end=' ', flush=True)


        try:
            x = all("certificate" in li for li in metadatas)
            certificate[i] = x
        except:
            if DEBUG:
                print('D2err' + str(i), end=' ', flush=True)
        
        
        try:
            x = 1
            for li in exe_data["coreReport"]["entries"]["entry_list"]:
                if "classification" in li:
                    if li["classification"]["classification"] == "Goodware":
                        x = 3
                    elif li["classification"]["classification"] == "Suspicious":
                        x = 2
                    else:
                        x = 0
                    break
            classification[i] = x
        except:
            if DEBUG:
                print('DD2err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(1 for li in exe_data["coreReport"]["entries"]["entry_list"]
                               if "tags" in li and "graylisting" in li["tags"]["tag_list"]))
            log_num_tags_graylisting[i] = x
        except:
            if DEBUG:
                print('E2err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(1 for li in exe_data["coreReport"]["entries"]["entry_list"]
                               if "tags" in li and "entropy" in li["tags"]["tag_list"]))
            log_num_tags_entropy[i] = x
        except:
            if DEBUG:
                print('F2err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + sum(int(li["info"]["file"]["size"],0)
                               for li in exe_data["coreReport"]["entries"]["entry_list"]
                               if "tags" in li and "entropy" in li["tags"]["tag_list"]))
            log_sum_tag_entropy_entry_sizes[i] = x
        except:
            if DEBUG:
                print('FF2err' + str(i), end=' ', flush=True)
        
        
        try:
            x = any("cert-malformed" in li["tags"]["tag_list"]
                    for li in exe_data["coreReport"]["entries"]["entry_list"]
                    if "tags" in li)
            cert_malformed[i] = x
        except:
            if DEBUG:
                print('G2err' + str(i), end=' ', flush=True)
        
        
        try:
            x = np.log(1 + len(exe_data["coreReport"]["relationships"]["entry_list"]))
            log_relationships_num[i] = x
        except:
            if DEBUG:
                print('H2err' + str(i), end=' ', flush=True)
        
        
        if (i%100 == 0):
            print(i, end=' ', flush=True)


    #---------------------------------------------#
    # Stvaranje DataFramea                        #
    #---------------------------------------------#
    
    data = {
        "name": [li.replace('/','.').replace('\\','.').split('.')[-2] for li in file_list],
        "log_entries_num": log_entries_num,
        "log_max_entry_size": log_max_entry_size,
        "log_average_entry_size": log_average_entry_size,
        "log_sum_entry_size": log_sum_entry_size,
        "log_repeated_entry_sizes": log_repeated_entry_sizes,
        "max_entry_entropy": max_entry_entropy,
        "average_entry_entropy": average_entry_entropy,
        "average2_entry_entropy": average2_entry_entropy,
        "warnings_num": warnings_num,
        "non_empty_metadatas": non_empty_metadatas,
        "max_elfa_new": max_elfa_new,
        "time_date_stamp_min_year": time_date_stamp_min_year,
        "time_date_stamp_max_year": time_date_stamp_max_year,
        "max_opt_header_size": max_opt_header_size,
        "characteristics_num": characteristics_num,
        "is_checksum_valid": is_checksum_valid,
        "log_max_size_of_initialized_data": log_max_size_of_initialized_data,
        "log_max_size_of_uninitialized_data": log_max_size_of_uninitialized_data,
        "diff_log_initialized_log_uninitialized": log_max_size_of_initialized_data -
                                                  log_max_size_of_uninitialized_data,
        "log_max_stack_reserve": log_max_stack_reserve,
        "log_max_heap_reserve": log_max_heap_reserve,
        "data_notnull_directories_num": data_notnull_directories_num,
        "first_section_name": first_section_name,
        "first_section_wec_code": first_section_wec_code,
        "log_sections_num": log_sections_num,
        "log_nonstandard_section_names_num": log_nonstandard_section_names_num,
        "log_sections_rwe_num": log_sections_rwe_num,
        "log_sections_rwec_num": log_sections_rwec_num,
        "last_section_discardable": last_section_discardable,
        "last_section_suspicious_name": last_section_suspicious_name,
        "log_max_section_size": log_max_section_size,
        "log_average_section_size": log_average_section_size,
        "log_zero_size_sections_num": log_zero_size_sections_num,
        "first_section_entropy": first_section_entropy,
        "max_section_entropy": max_section_entropy,
        "average2_section_entropy": average2_section_entropy,
        "log_max_section_suspiciousness": log_max_section_suspiciousness,
        "log_imports_num": log_imports_num,
        "log_max_api_list_size": log_max_api_list_size,
        "log_average_api_list_size": log_average_api_list_size,
        "log_sum_api_list_size": log_sum_api_list_size,
        "contains_codeviews": contains_codeviews,
        "log_overlay_size": log_overlay_size,
        "entry_minus_sections_minus_overlay": entry_minus_sections_minus_overlay,
        "rich_header_valid": rich_header_valid,
        "log_sum_rich_header_size": log_sum_rich_header_size,
        "log_rich_header_entries_num": log_rich_header_entries_num,
        "log_rich_header_count_max": log_rich_header_count_max,
        "log_rich_header_count_avg": log_rich_header_count_avg,
        "log_rich_header_count_sum": log_rich_header_count_sum,
        "protection": protection,
        "certificate": certificate,
        "classification": classification,
        "log_num_tags_graylisting": log_num_tags_graylisting,
        "log_num_tags_entropy": log_num_tags_entropy,
        "log_sum_tag_entropy_entry_sizes": log_sum_tag_entropy_entry_sizes,
        "log_total_minus_entropy_size": log_sum_entry_size -
                                        log_sum_tag_entropy_entry_sizes,
        "cert_malformed": cert_malformed,
        "log_relationships_num": log_relationships_num,
    }

    df = pd.DataFrame(data, columns = data)
    df.index.name = 'index'

    return df
