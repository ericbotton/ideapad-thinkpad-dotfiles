# Function to recursively get files and folders
function Get-FilesAndFolders {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, ValueFromPipelineByPropertyName = $true)]
        [Alias('FullName')]
        [string]$Path,

        [Parameter()]
        [string[]]$ExcludeFolders
    )

    process {
        if (Test-Path -Path $Path) {
            # Get the current folder
            $currentFolder = Get-Item -Path $Path

            # Get all the files in the current folder
            $files = Get-ChildItem -LiteralPath $currentFolder.FullName -File

            # Sort files by modification time
            $sortedFiles = $files | Sort-Object -Property LastWriteTime

            foreach ($file in $sortedFiles) {
                # $relativePath = $file.FullName.Substring($currentFolder.FullName.Length + 1)
                $output = @{
                    # 'RelativePath' = $relativePath
                    'DateModified' = $file.LastWriteTime
                    'FullPath' = $file.FullName
                }
 
                Write-Output $output
            }

            # Get all the subfolders in the current folder
            $subfolders = Get-ChildItem -LiteralPath $currentFolder.FullName -Directory

            foreach ($subfolder in $subfolders) {
                if ($subfolder.FullName -notin $ExcludeFolders) {
                    Get-FilesAndFolders -Path $subfolder.FullName -ExcludeFolders $ExcludeFolders
                }
            }
        }
    }
}

# Usage example
$rootPath = "C:\Users\Owner\"
$excludeFolders = @("", "")
$output = Get-FilesAndFolders -Path $rootPath -ExcludeFolders $excludeFolders | Sort-Object -Property DateModified
$output
