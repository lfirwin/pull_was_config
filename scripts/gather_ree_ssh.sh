#!/bin/bash
#-----------------------------------------------------------------------------------------
# This script does the actual gathering of WPP configuration data by submitting commands
# to the various environment deployment manager hosts via ssh.  In order for this 
# script to work without human interaction, the id_dsa.pub key needs to be the 
# authorized_keys on the target host.
#
# This script copies the Jython script to the target host, executes it, and copies the
# resulting file back, does a diff between the existing html file and the generated one, 
# and only replaces the existing file if the new one is different and no error was 
# generated on the target host when running the Jython script.
#
# Input Parameters:
#   This script takes 1 parameter:
#      n - where n is a number representing the index of the environment in the 
#          environments array.
#-----------------------------------------------------------------------------------------

# Include the properties file
. /service/config-data/wpp-ree/scripts/gather_ree.props

# Create a temporary html file for an environment if there were errors
function create_temp
{
   echo "<!DOCTYPE html>" > "${tmp}/html/${name}.html"
   echo "<html>" >> "${tmp}/html/${name}.html"
   echo "<head>" >> "${tmp}/html/${name}.html"
   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"./style.css\">" >> "${tmp}/html/${name}.html"
   echo "<title>${title}</title>" >> "${tmp}/html/${name}.html"
   echo "</head>" >> "${tmp}/html/${name}.html"
   echo "<body>" >> "${tmp}/html/${name}.html"
   echo "<div class=\"update\">" >> "${tmp}/html/${name}.html"
   echo "<a class=\"home\" href=\"./index.html\">Home</a></br>" >> "${tmp}/html/${name}.html"
   echo "Updated:" >> "${tmp}/html/${name}.html"
   echo "<script>" >> "${tmp}/html/${name}.html"
   echo "document.write(document.lastModified);" >> "${tmp}/html/${name}.html"
   echo "</script>" >> "${tmp}/html/${name}.html"
   echo "</div>" >> "${tmp}/html/${name}.html"
   echo "<h3>${title}: <a href=\"${console}\">${console}</a></h3>" >> "${tmp}/html/${name}.html"
   echo "<h4>Resource Environment Entries</h4>" >> "${tmp}/html/${name}.html"
   echo "<table>" >> "${tmp}/html/${name}.html"
   echo "  <tr>" >> "${tmp}/html/${name}.html"
   echo "    <th colspan=2 align=left>None</th>" >> "${tmp}/html/${name}.html"
   echo "  </tr>" >> "${tmp}/html/${name}.html"
   echo "  <tr><td colspan=2>&nbsp;</td></tr>" >> "${tmp}/html/${name}.html"
   echo "</table>" >> "${tmp}/html/${name}.html"
   echo "<h4>URLs</h4>" >> "${tmp}/html/${name}.html"
   echo "<table>" >> "${tmp}/html/${name}.html"
   echo "  <tr>" >> "${tmp}/html/${name}.html"
   echo "    <th colspan=2 align=left>None</th>" >> "${tmp}/html/${name}.html"
   echo "  </tr>" >> "${tmp}/html/${name}.html"
   echo "  <tr><td colspan=2>&nbsp;</td></tr>" >> "${tmp}/html/${name}.html"
   echo "</table>" >> "${tmp}/html/${name}.html"
   echo "</body>" >> "${tmp}/html/${name}.html"
   echo "</html>" >> "${tmp}/html/${name}.html"

   if [ ! -f "${home}/${name}.html" ]
   then
      cp "${tmp}/html/${name}.html" "${home}/${name}.html"
   fi
}

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

# Copy and edit soap.client.props file
function copy_soap_client_props
{
   soap_props=""
   exists=`ssh -q wasadm@${host} "if [ -f /apps/scripts/ree/${name}-soap.client.props ]; then if [ -s /apps/scripts/ree/${name}-soap.client.props ]; then echo yes; else echo ''; fi; fi"`
   if [ -n "${exists}" ]
   then
      props="/apps/scripts/ree/${name}-soap.client.props"
      old_props="${was_bin%/bin}/properties/soap.client.props"
      user="$(ssh -q wasadm@${host} "grep com.ibm.SOAP.loginUserid ${props}")"
      old_user="$(ssh -q wasadm@${host} "grep com.ibm.SOAP.loginUserid ${old_props}")"
      password="$(ssh -q wasadm@${host} "grep com.ibm.SOAP.loginPassword ${props}")"
      old_password="$(ssh -q wasadm@${host} "grep com.ibm.SOAP.loginPassword ${old_props}")"
      if [ "${user}" != "${old_user}" ]
      then
         echo "Updating user...."
         ssh -q wasadm@${host} "sed 's/com.ibm.SOAP.loginUserid.*/com.ibm.SOAP.loginUserid=${old_user}/' ${props} > /apps/scripts/ree/${name}-soap.client.tmp"
         ssh -q wasadm@${host} "cp /apps/scripts/ree/${name}-soap.client.tmp /apps/scripts/ree/${name}-soap.client.props"
      fi  
      if [ "${password}" != "${old_password}" ]
      then
         echo "Updating password..."
         ssh -q wasadm@${host} "sed 's/com.ibm.SOAP.loginPassword.*/com.ibm.SOAP.loginPassword=${old_user}/' ${props} > /apps/scripts/ree/${name}-soap.client.tmp"
         ssh -q wasadm@${host} "cp /apps/scripts/ree/${name}-soap.client.tmp /apps/scripts/ree/${name}-soap.client.props"
      fi  
      timeout=`ssh -q wasadm@${host} "grep com.ibm.SOAP.requestTimeout ${props}"`
      OIFS=$IFS
      IFS="="
      parts=(${timeout})
      IFS=OIFS
      if [ "${parts[1]}" != "9000" ]
      then
         echo "Updating timeout..."
         ssh -q wasadm@${host} "sed 's/com.ibm.SOAP.requestTimeout.*/com.ibm.SOAP.requestTimeout=9000/' ${props}> /apps/scripts/ree/${name}-soap.client.tmp"
         ssh -q wasadm@${host} "cp /apps/scripts/ree/${name}-soap.client.tmp /apps/scripts/ree/${name}-soap.client.props"
      fi  
      ssh -q wasadm@${host} "rm -f /apps/scripts/ree/${name}-soap.client.tmp"
      ssh -q wasadm@${host} "echo com.ibm.SOAP.ConfigURL=file:/apps/scripts/ree/${name}-soap.client.props > /apps/scripts/ree/${name}-override-soap.props" 
      soap_props="-p /apps/scripts/ree/${name}-override-soap.props"
   else
      echo "file found..."
      props="${was_bin%/bin}/properties/soap.client.props"
      timeout=`ssh -q wasadm@${host} "grep com.ibm.SOAP.requestTimeout ${props}"`
      OIFS=$IFS
      IFS="="
      parts=(${timeout})
      IFS=OIFS
      if [ "${parts[1]}" != "9000" ]
      then
         echo "Updating timeout..."
         ssh -q wasadm@${host} "sed 's/com.ibm.SOAP.requestTimeout.*/com.ibm.SOAP.requestTimeout=9000/' ${props} > /apps/scripts/ree/${name}-soap.client.props"
         ssh -q wasadm@${host} "echo com.ibm.SOAP.ConfigURL=file:/apps/scripts/ree/${name}-soap.client.props > /apps/scripts/ree/${name}-override-soap.props"
         soap_props="-p /apps/scripts/ree/${name}-override-soap.props"
      fi  
   fi
}

#-----------------------------------------------------------------------------------------
# Main Script Logic
#-----------------------------------------------------------------------------------------
# Get the script and directory names
script=`basename "${0}" _ssh.sh`
dir=`dirname "${0}"`
jy_script="${script}.py"

# Set the index of the environments array
i=${1}

echo "before parse environment"
# Parse environment information
parse_env

echo "after parse..."
# Compose the console URL string
console="https://${host}:${https_port}/ibm/console"

# Get the start timestamp for the script
start=$(date)
echo "Gathering Configuration Info for ${title} on ${host} at ${start}..."

# Copy Jython script
ssh -o BatchMode=yes -q wasadm@${host} "ls ${local_scripts}" > /dev/null

# Check for error with ssh
if [ $? -ne 0 ]
then
   echo "${name}.html - error connecting via ssh on ${start}" >> ${log}
   exit    
fi

# Make the script directory if it doesn't exist
scripts=`ssh -o BatchMode=yes -q wasadm@${host} "ls ${local_scripts}"`
if [ -z "${scripts}" ]
then
   ssh -q wasadm@${host} "mkdir -p ${local_scripts}" 
fi

# Copy the Jython script
scp -q "${dir}/${jy_script}" wasadm@${host}:${local_scripts}

# Delete the html file on the host
ssh wasadm@${host} "rm -f ${tmp}/${name}.html"

# Copy the soap.client.props file if needed
copy_soap_client_props

# Execute the Jython script
echo;echo "Executing..." 
#echo "${was_bin}/wsadmin.sh -lang jython -conntype SOAP -f ${local_scripts}/${jy_script} \"${title}\" ${tmp}/${name}.html ${tmp}/${name}.xml \"${console}\""
#ssh -q wasadm@${host} "${was_bin}/wsadmin.sh -lang jython -conntype SOAP -f ${local_scripts}/${jy_script} \"${title}\" ${tmp}/${name}.html ${tmp}/${name}.xml \"${console}\""

echo "${was_bin}/wsadmin.sh -lang jython -conntype SOAP ${soap_props} -f ${local_scripts}/${jy_script} \"${title}\" ${tmp}/${name}.html ${tmp}/${name}.xml \"${console}\""
ssh -q wasadm@${host} "${was_bin}/wsadmin.sh -lang jython -conntype SOAP ${soap_props} -f ${local_scripts}/${jy_script} \"${title}\" ${tmp}/${name}.html ${tmp}/${name}.xml \"${console}\""

# Save the return code
rc=$?

# Record the end timestamp
end=$(date +"%D @ %T")

# Check the return code 
if [ $rc -eq 0 ]
then
   # Did the html file get generated?
   echo "Checking for ${name}.html file on ${host}..."
   if ssh -q wasadm@${host} "ls ${tmp}/${name}.html" > /dev/null 2>&1
   then
      # Copy the file to a temp directory on this host
      echo "   The ${name}.html exists, copying here."
      source="${tmp}/${name}.html" 
      #scp -q wasadm@${host}:${tmp}/${name}.html ${tmp}/html
      scp -q wasadm@${host}:${source} ${tmp}/html
      
      # Compare generated file and existing file
      echo "   Comparing new file to existing file..."
      if [ -f "${home}/${name}.html" ]
      then
         # Run a diff between the two files
         diff=`diff "${home}/${name}.html" "${tmp}/html/${name}.html" | wc -l`
         if [ ${diff} -gt 0 ]
         then
            # Replace existing file with generated file
            echo "      New file is different, replacing old file."
            cp "${tmp}/html/${name}.html" ${home}
            echo "${name}.html - updated on ${end}" >> ${log}
         else # Files are the same, no need to copy
            echo "      Files are the same."
            echo "${name}.html - checked and no update on ${end}" >> ${log}
         fi
      else  # No existing file so copy generated file
         echo "      No old file, copying new file."
         cp "${tmp}/html/${name}.html" ${home}
         echo "${name}.html - updated on ${end}" >> ${log}
      fi
   else # File not generated
      # Create the temp file
      echo "   File ${name}.html does not exist on ${host}."
      echo "      Creating a default ${name}.html file as a place holder."
      create_temp
      echo "${name}.html - error updating on ${end}" >> ${log}
   fi

   # Copy the xml file
   echo
   echo "Checking for ${name}.xml file on ${host}..."
   if ssh -q wasadm@${host} "ls ${tmp}/${name}.xml" > /dev/null 2>&1
   then
      # Copy the file to a temp directory on this host
      echo "   The ${name}.xml exists, copying here."
      scp -q wasadm@${host}:${tmp}/${name}.xml ${tmp}/html

      # Compare generated file and existing file
      echo "   Comparing new file to existing file..."
      if [ -f "${home}/${name}.xml" ]
      then
         # Run a diff between the two files
         diff "${tmp}/html/${name}.xml" <(sed '/<lastmod>/d' "${home}/${name}.xml") > /dev/null
         diffs=$?
         
         if [ ${diffs} -gt 0 ]
         then
            # Replace existing file with generated file
            echo "      New file is different, replacing old file."
            cp "${tmp}/html/${name}.xml" "${home}"
            sed -i'' '$ d' "${home}/${name}.xml"
            echo "  <lastmod>${end}</lastmod>" >> "${home}/${name}.xml"
            echo "</cell>" >> "${home}/${name}.xml"            
            echo "${name}.xml - updated on ${end}" >> ${log}
         else # Files are the same, no need to copy
            echo "      Files are the same."
            echo "${name}.xml - checked and no update on ${end}" >> ${log}
            grep lastmod "${home}/${name}.xml" > /dev/null
            if [ $? -gt 0 ]
            then
               sed -i'' '$ d' "${home}/${name}.xml"
               echo "  <lastmod>${end}</lastmod>" >> "${home}/${name}.xml"
               echo "</cell>" >> "${home}/${name}.xml"            
            fi
         fi
      else  # No existing file so copy generated file
         echo "      No old file, copying new file."
         cp "${tmp}/html/${name}.xml" "${home}"
         sed -i'' '$ d' "${home}/${name}.xml"
         echo "  <lastmod>${end}</lastmod>" >> "${home}/${name}.xml"
         echo "</cell>" >> "${home}/${name}.xml"            
         echo "${name}.xml - updated on ${end}" >> ${log}
      fi
   fi
else # Error occurred during execution of the Jython script
   # Create the temp file
   echo "There was an error while running the Jython script.  Not copying HTML file."
   echo "      Creating a default ${name}.html file as a place holder."
   create_temp
   echo "${name}.html - error updating on ${end}" >> ${log}
fi

echo "Finished Gathering Configuration Info for ${title} on ${host} at ${end}..."
echo 
