#!/bin/bash
#-----------------------------------------------------------------------------------------
# This script acts as the master script to gather configuration information for WPP
# environments.  This script creates the index.html and log.html files and controls
# execution of the gather_ree_ssh.sh script that does the actual gathering of the data.
#
# Input parameters:
#   This script takes 1 or no parameters.  The single parameter can be one of the
#   following:
#      n - where n is a number representing the index of the environment in the 
#          environments array.
#      index - create the index.html file only
#      log - create the log.html file only
#      no parameter - gather from all environments, create the index.html and log.html
#                     files.
#-----------------------------------------------------------------------------------------

# Include the properties file
. /service/config-data/wpp-ree/scripts/gather_ree.props

# Parse the current Environment array element
function parse_env
{
   # Parse environment information
   temp="${envs[$i]}"
   OIFS=$IFS
   IFS="|"
   env=(${temp})
   IFS=OIFS
   count="${#env[@]}"

   name="${env[0]}"
   title="${env[1]}"
   host="${env[2]}"
   OIFS=$IFS
   IFS="."
   host_parts=(${host})
   IFS=OIFS
   host_short="${host_parts[0]}"
   https_port="${env[3]}"
   was_bin="${env[4]}"
}

# Generate the log.html file
function gen_log
{
   echo "<!DOCTYPE html>" > ${log_html}
   echo "<html>" >> ${log_html}
   echo "<head>" >> ${log_html}
   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"./style.css\">" >> ${log_html}
   echo "<title>WPP Configuration Dashboard Log</title>" >> ${log_html}
   echo "</head>" >> ${log_html}
   echo "<body>" >> ${log_html}
   echo "<div class=\"update\">" >> ${log_html}
   echo "<a class=\"home\" href=\"config-index.html\">Home</a></br>" >> ${log_html}
   echo "Updated:" >> ${log_html}
   echo "<script>" >> ${log_html}
   echo "document.write(document.lastModified);" >> ${log_html}
   echo "</script>" >> ${log_html}
   echo "</div>" >> ${log_html}
   echo "<h1>Log</h1>" >> ${log_html}

   # Iterate through the environments array writing the corresponding log entry to 
   # log.html
   counter="${#envs[@]}"
   i=0
   while [ ${i} -lt ${counter} ]
   do
      parse_env
      echo "Generating log entry for ${title}..."
      entry=$(grep ${name}.html ${log})
      if grep -q "error" <<< "${entry}"
      then
         echo "<span style=\"color: red;font-style:italic;\">${entry}</span><br/>" >> ${log_html}
      else
         echo "${entry}<br/>" >> ${log_html}
      fi
      let i=i+1
   done

   echo "</u>" >> ${log_html}
   echo "</div>" >> ${log_html}
   echo "</body>" >> ${log_html}
   echo "</html>" >> ${log_html}
}

# Generate the index.html file
function gen_index
{
   echo "<!DOCTYPE html>" > ${tmp_index}
   echo "<html>" >> ${tmp_index}
   echo "<head>" >> ${tmp_index}
   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"./style.css\">" >> ${tmp_index}
   echo "<title>WPP Configuration Dashboard</title>" >> ${tmp_index}
   echo "</head>" >> ${tmp_index}
   echo "<body>" >> ${tmp_index}
   echo "<div class=\"update\">" >> ${tmp_index}
   echo "<a class=\"home\" href=\"log.html\">Log</a>" >> ${tmp_index}
   echo "Updated:" >> ${tmp_index}
   echo "<script>" >> ${tmp_index}
   echo "document.write(document.lastModified);" >> ${tmp_index}
   echo "</script>" >> ${tmp_index}
   echo "</div>" >> ${tmp_index}
   echo "<h1> Environments</h1>" >> ${tmp_index}
   echo "<div class=\"nav\">" >> ${tmp_index}

   # Iterate through the environments array writing the corresponding log entry to 
   # index.html
   counter="${#envs[@]}"
   i=0
   server=""
   echo ${counter}
   while [ ${i} -lt ${counter} ]
   do
      parse_env
      echo "Generating link for ${title} on ${host}..."
      
      # Group entries by host
      if [ "${host}" != "${server}" ]
      then
         if [ -n "${server}" ]
         then
            echo "</ul>" >> ${tmp_index}
         fi
         echo "${host_short}" >> ${tmp_index}
         echo "<ul class=\"nav\">" >> ${tmp_index}
         server="${host}"
      fi
      echo "<li><a href=\"./${name}.html\"><b>${title}</b></a>: <a href=\"./${name}.html#scope\">scope</a> | <a href=\"./${name}.html#server_config\">server config</a> | <a href=\"./${name}.html#datasources\">data sources</a> | <a href=\"./${name}.html#mqcf\">mq conn factories</a> | <a href=\"./${name}.html#mqqueue\">mq queues</a> | <a href=\"./${name}.html#j2cconn\">j2c conn factories</a> | <a href=\"./${name}.html#j2cqueue\">j2c queues</a> | <a href=\"./${name}.html#actspecs\">activation specs</a> | <a href=\"./${name}.html#rees\">rees</a> | <a href=\"./${name}.html#urls\">urls</a> | <a href=\"./${name}.html#libraries\">shared libraries</a> | <a href=\"./${name}.html#variables\">variables</a> | <a href=\"./${name}.html#vhosts\">virtual hosts</a></li>" >> ${tmp_index}
      let i=i+1
   done

   echo "</u>" >> ${tmp_index}
   echo "</div>" >> ${tmp_index}
   echo "</body>" >> ${tmp_index}
   echo "</html>" >> ${tmp_index}

   # Replace the index.html only if it has changed.
   if [ -f "${tmp_index}" ]
   then
      if [ -f "${home}/${index}" ]
      then
         diff=`diff "${home}/${index}" "${tmp_index}" | wc -l`
         if [ ${diff} -gt 0 ]
         then
            cp "${tmp_index}" ${home}
            sed 's/\.html/\.xml/g' ${tmp_index} > ${home}/${xml_index}
         fi
      else
         cp "${tmp_index}" ${home}
         sed 's/\.html/\.xml/g' ${tmp_index} > ${home}/${xml_index}
      fi
   fi
}

#-----------------------------------------------------------------------------------------
# Main Script Logic
#-----------------------------------------------------------------------------------------

# Get the script and directory names
script=`basename "${0}" .sh`
dir=`dirname "${0}"`
jy_script="${script}.py"

# Verify the environments array is populated
if [ -z "${envs}" ]
then
   exit
fi

# Clean up temp html folder
if [ -d "${tmp}/html" -o -f "${tmp}/html" ]
then
   rm -rf "${tmp}/html"
fi
mkdir "${tmp}/html"

# Set environments array index and counter dependent on input parms
if [ $# -eq 1 -a "${1}" != "index" -a "${1}" != "log" ]
then
   i=${1}
   let counter=i+1
else
   counter="${#envs[@]}"
   i=0
fi

# Generate index.html file if requested and exit
if [ $# -eq 1 -a "${1}" = "index" ]
then
   gen_index
   exit
fi

# Generate log.html file if requested and exit
if [ $# -eq 1 -a "${1}" = "log" ]
then
   gen_log
   exit
fi

# Copy environments array
run=("${envs[@]}")

# Init loop control variables
num_proc=0
submitted=${i}

# Iterate through the run array until all environments are submitted
while [ ${submitted} -lt ${counter} ]
do
   # Set start index
   start_index=-1
   
   # Iterate through the run array
   while [ ${i} -lt ${counter} ]
   do
      # Check if this entry has been submitted yet
      if [ "${run[$i]}" != "done" ]
      then
         # Get number of gather_ree_ssh.sh scripts running
         num_proc=$(ps -ef|grep gather_ree_ssh.sh|grep -v grep|wc -l)
         # Check if max number of processes running
         if [ ${num_proc} -lt 9 ]
         then
            # Parse the environment entry
            parse_env
            # Check if gather_ree_ssh.sh script already running on this host
            num_hosts=$(ps -ef|grep ${host}|grep -v grep|wc -l)
            if [ ${num_hosts} -eq 0 ]
            then
               # Remove this entry from the log file
               sed -i.bak "/${name}/d" ${log}
               # Run the gather_ree_ssh.sh script
               if [ $# -eq 1 ]
               then
                  ${dir}/gather_ree_ssh.sh ${i} &
               else
                  echo "Gathering Configuration Info for ${title} on ${host}..."
                  ${dir}/gather_ree_ssh.sh ${i} > ${tmp}/gather_ree_ssh.out.${i} 2>&1 &
               fi
               run[i]="done"
               let submitted=submitted+1
            else # Script already running on this host
               # Save the current index as the start index for next iteration through
               if [ ${start_index} -eq -1 ]
               then
                  start_index=${i}
               fi
            fi
         else # Max number of processes running
            # Save the current index as the start index for next iteration through
            if [ ${start_index} -eq -1 ]
            then
               start_index=${i}
            fi
            # Break out of iteration
            break
         fi
      fi
      let i=i+1
   done
   # Set the index for the next iteration
   if [ ${start_index} -ge 0 ]
   then
      i=${start_index}
   fi
   # Pause for 15 seconds
   if [ ${submitted} -lt ${counter} ]
   then
      sleep 15
   fi
done            

# Wait for submitted gather_ree_ssh.sh scripts to finish processing
wait

# Generate index.html and log.html
if [ $# -eq 0 ]
then
   gen_index 

   cat ${tmp}/gather_ree_ssh.out.* > ${dir}/gather_ree_ssh.out
   rm -f ${tmp}/gather_ree_ssh.out.*
fi

# Generate log.html
gen_log

# Set permissions for the html files
chmod 644 ${home}/*.html

